import datetime
import time
import os
import logging
import random  # for generating scoring requests
import requests
import json
from retry import retry
from ibm_ai_openscale import APIClient, APIClient4ICP, WatsonMachineLearningInstance4ICP
from ibm_ai_openscale.engines import WatsonMachineLearningInstance, WatsonMachineLearningAsset
from ibm_ai_openscale.supporting_classes import PayloadRecord
from ibm_ai_openscale_cli.ml_engines.watson_machine_learning.models.drug_selection_model import DrugSelectionModel
from ibm_ai_openscale_cli.utils import get_iam_headers

logger = logging.getLogger(__name__)
parent_dir = os.path.dirname(__file__)

class AIOSClient():

    def __init__(self, credentials, datamart_name, history_days, target_env):
        self._credentials = credentials
        self._datamart_name = target_env['datamart_name'] if datamart_name == 'aiosfastpath' else datamart_name
        self._history_days = history_days
        self._target_env = target_env
        self._model = DrugSelectionModel(target_env)
        self._client = None
        self._is_icp = True if self._target_env['name'].lower() == 'icp' else False
        self._verify = False if self._is_icp else True
        if self._is_icp:
            self._client = APIClient4ICP(credentials)
        else:
            self._client = APIClient(credentials)
        logger.info('Using AI Openscale (AIOS) Python Client version: {}'.format(self._client.version))

    @retry(tries=5, delay=4, backoff=2)
    def clean_datamart(self):
        logger.info('Clean up datamart, if already present: {}'.format(self._datamart_name))
        subscriptions_uids = self._client.data_mart.subscriptions.get_uids()

        # clean up all subscriptions in the datamart
        for subscription_uid in subscriptions_uids:
            # disable explainability, fairness checking, and payload logging for the subscription
            subscription = self._client.data_mart.subscriptions.get(subscription_uid)
            subscription.explainability.disable()
            subscription.fairness_monitoring.disable()
            subscription.payload_logging.disable()
            # then remove the subscription itself
            self._client.data_mart.subscriptions.delete(subscription_uid)

        # remove bindings
        try:
            bindings_uids = self._client.data_mart.bindings.get_uids()
            for binding_uid in bindings_uids:
                self._client.data_mart.bindings.delete(binding_uid)
        except:
            logger.warn('datamart bindings could not be deleted')

        # remove previous datamart
        try:
            self._client.data_mart.delete()
        except Exception as e:
            if 'AISCS0005W' in str(e): # datamart does not exist, so cannot delete
                logger.debug(e)
            else:
                raise e

    @retry(tries=5, delay=8, backoff=2)
    def create_datamart(self, database_credentials):
        '''
        Create datamart schema and datamart
        '''
        logger.info('Create datamart: {}'.format(self._datamart_name))

        if database_credentials is None:
            logger.info('AIOS PostgreSQL instance: internal')
            self._client.data_mart.setup(internal_db=True)
        else:
            database = None
            if database_credentials['uri'].startswith('postgres:'):
                from ibm_ai_openscale_cli.database_clases.postgres import Postgres
                database = Postgres(database_credentials)
            elif database_credentials['uri'].startswith('db2:'):
                from ibm_ai_openscale_cli.database_clases.db2 import DB2
                database = DB2(database_credentials)
            else:
                raise Exception('Invalid database type specified. Only "postgresql" and "db2" are supported.')
            database.drop_existing_schema(self._datamart_name)
            database.create_new_schema(self._datamart_name)
            self._client.data_mart.setup(db_credentials=database_credentials, schema=self._datamart_name)

        logger.info('Datamart {} created'.format(self._datamart_name))

    @retry(tries=5, delay=4, backoff=2)
    def bind_mlinstance(self, wml_credentials):
        '''
        Bind ML instance to AIOS
        '''
        logger.info('Bind WML instance to AIOS')
        binding_name = None
        if self._is_icp:
            wml_instance = WatsonMachineLearningInstance4ICP()
            binding_name = 'WML ICP instance'
        else:
            wml_instance =  WatsonMachineLearningInstance(wml_credentials)
            binding_name = 'WML instance'
        return self._client.data_mart.bindings.add(binding_name, wml_instance)

    @retry(tries=5, delay=4, backoff=2)
    def register_model(self, model_deployment):
        '''
        Create subscription in AIOS for drug-selection model
        Configure payload logging plus performance, fairness, explainability, and accuracy monitoring
        '''
        logger.info('Register ML instance to AIOS: {}'.format(model_deployment['model_name']))
        subscription = self._add_subscription(WatsonMachineLearningAsset(model_deployment['model_guid']))
        self.configure_subscription(model_deployment, subscription)
        return subscription

    @retry(tries=5, delay=4, backoff=2)
    def _add_subscription(self, asset):
        return self._client.data_mart.subscriptions.add(asset)

    @retry(tries=5, delay=8, backoff=2)
    def configure_subscription(self, model_deployment, subscription):
        model_name = model_deployment['model_name']

        logger.info('Enable payload logging in AIOS: {}'.format(model_name))
        subscription.payload_logging.enable()

        logger.info('Enable Performance Monitoring in AIOS: {}'.format(model_name))
        subscription.performance_monitoring.enable()

        logger.info('Configuring fairness monitoring for model: {}'.format(model_name))
        fairness_monitoring_params = self._model.get_fairness_monitoring_params()
        subscription.fairness_monitoring.enable(
            features=fairness_monitoring_params['features'],
            prediction_column=fairness_monitoring_params['prediction_column'],
            favourable_classes=fairness_monitoring_params['favourable_classes'],
            unfavourable_classes=fairness_monitoring_params['unfavourable_classes'],
            min_records=40
        )

        logger.info('Configuring accuracy monitoring for model: {}'.format(model_name))
        subscription.quality_monitoring.enable(problem_type='multiclass', threshold=0.8, min_records=40)

        feedback_params = self._model.get_feedback_params()
        subscription.feedback_logging.store(feedback_params['values'], fields=feedback_params['fields'])

        logger.info('Configuring explainability monitoring for model: {}'.format(model_name))
        iamHeaders = get_iam_headers(self._credentials, self._target_env)
        expBody = self.get_explainability_body(
            model_deployment,
            subscription.binding_uid,
            self._model.get_explainability_params()
        )
        url = self._credentials['url'] + '/v1/model_explanation_configurations'
        reply = requests.post(url, json=expBody, headers=iamHeaders, verify=self._verify)
        reply.raise_for_status()

    @retry(tries=5, delay=4, backoff=2)
    def generate_sample_scoring(self, model_deployment, bindingGuid, subscription):
        '''
        Generate historical data
        Generate sample scoring requests
        Trigger fairness check
        '''
        model_name = model_deployment['model_name']
        model_guid = model_deployment['model_guid']
        deployment_guid = model_deployment['deployment_guid']
        metricsurl = '{0}/v1/data_marts/{1}/metrics'.format(self._credentials['url'], self._credentials['data_mart_id'])
        iam_headers = get_iam_headers(self._credentials, self._target_env)

        wml_client = self._client.data_mart.bindings.get_native_engine_client(binding_uid=bindingGuid)
        deployment_details = wml_client.deployments.get_details(deployment_guid)
        deployment_url = wml_client.deployments.get_scoring_url(deployment_details)

        logger.info('Load historical scoring records to Payload Logging and MeasurementFacts tables in AIOS: {}'.format(model_name))
        historyfile = self._model.get_history_payload_file()

        if historyfile != None:
            with open(historyfile) as f:
                payloads = json.load(f)
            for day in range(self._history_days):
                logger.info('Loading day {}'.format(day+1))
                for hour in range(24):
                    # store payload logging history in Payload table
                    recordsList = []
                    for payload in payloads:
                        score_time = str(datetime.datetime.utcnow() + datetime.timedelta(hours=(-(24*day + hour + 1))))
                        recordsList.append(PayloadRecord(request=payload['request'], response=payload['response'], scoring_timestamp=score_time))
                    # Retry a specific failure point
                    self.reliable_load(subscription, recordsList)

                    # store performance monitor history in MeasurementFacts table
                    score_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=(-(24*day + hour + 1)))).strftime('%Y-%m-%dT%H:%M:%SZ')
                    score_count = random.randint(60, 600)
                    score_resp = random.uniform(60, 300)
                    performanceMetric = {
                        'metric_type': 'performance',
                        'binding_id': bindingGuid,
                        'timestamp': score_time,
                        'subscription_id': model_guid,
                        'asset_revision': model_guid,
                        'deployment_id': deployment_guid,
                        'value': {
                            'response_time': score_resp,
                            'records': score_count
                        }
                    }
                    requests.post(metricsurl, json=[performanceMetric], headers=iam_headers, verify=self._verify)

        logger.info('Load historical fairness MeasurementFacts to AIOS: {}'.format(model_name))
        historyfile = self._model.get_history_fairness_file()
        if historyfile != None:
            with open(historyfile) as f:
                fairnessValues = json.load(f)
            for day in range(self._history_days):
                logger.info('Loading day {}'.format(day+1))
                for hour in range(24):
                    fairnessTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=(-(24*day + hour + 1)))).strftime('%Y-%m-%dT%H:%M:%SZ')
                    fairnessMetric = {
                        'metric_type': 'fairness',
                        'binding_id': bindingGuid,
                        'timestamp': fairnessTime,
                        'subscription_id': model_guid,
                        'asset_revision': model_guid,
                        'deployment_id': deployment_guid,
                        'value': fairnessValues[random.randint(0, len(fairnessValues))-1]
                    }
                    requests.post(metricsurl, json=[fairnessMetric], headers=iam_headers, verify=self._verify)

        logger.info('Load historical quality MeasurementFacts to AIOS: {}'.format(model_name))
        for day in range(self._history_days):
            logger.info('Loading day {}'.format(day+1))
            for hour in range(24):
                qualityTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=(-(24*day + hour + 1)))).strftime('%Y-%m-%dT%H:%M:%SZ')
                quality = random.uniform(0.75, 0.95)
                qualityMetric = {
                    'metric_type': 'quality',
                    'binding_id': bindingGuid,
                    'timestamp': qualityTime,
                    'subscription_id': model_guid,
                    'asset_revision': model_guid,
                    'value': {
                        'quality': quality,
                        'threshold': 0.8,
                        'metrics': [
                            {
                                'name': 'auroc',
                                'value': quality,
                                'threshold': 0.8
                            }
                        ]
                    }
                }
                self.reliable_post_metrics(metricsurl, iam_headers, qualityMetric)

        numscores = 100
        logger.info('Generate {} new scoring requests to AIOS: {}'.format(numscores, model_name))
        if self._is_icp and ':31002' not in deployment_url:
                deployment_url_host = ':'.join(deployment_url.split(':')[:2])
                args_url_host = ':'.join(self._target_env['aios_url'].split(':')[:2])
                deployment_url = deployment_url.replace('{}:16600'.format(deployment_url_host), '{}:31002'.format(args_url_host))
        for _ in range(numscores):
            wml_client.deployments.score(deployment_url, self._model.get_score_input())

        logger.info('Trigger immediate fairness check AIOS: {}'.format(model_name))
        subscription.fairness_monitoring.run()

        logger.info('Trigger immediate quality check AIOS: {}'.format(model_name))
        subscription.quality_monitoring.run()

    @retry(tries=5, delay=4, backoff=2)
    def reliable_load(self, subscription, records_list):
        '''
        Retry the loading code so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        return subscription.payload_logging.store(records=records_list)

    @retry(tries=5, delay=4, backoff=2)
    def reliable_post_metrics(self, metrics_url, iam_headers, quality_metric):
        '''
        Retry the loading metrics so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        return requests.post(metrics_url, json=[quality_metric], headers=iam_headers, verify=self._verify)

    def get_explainability_body(self, model_deployment, service_binding_uid, categorical_columns):
        model_metadata = model_deployment['model_metadata_dict']
        feature_columns = [d.get('name') for d in model_metadata['training_data_schema']
                           ['fields'] if d.get('name') != model_metadata['label_column']]
        exp_body = {
            'data_mart_id': self._credentials['data_mart_id'],
            'service_binding_id': service_binding_uid,
            'model_id': model_deployment['model_guid'],
            'parameters': {
                'model_type': model_metadata['evaluation']['method'],
                'model_data_type': 'numeric_categorical',
                'model_source': 'wml',
                'label_column': model_metadata['label_column'],
                'feature_columns': feature_columns,
                'categorical_columns': categorical_columns,
                'training_data_reference': model_metadata['training_data_reference'][0]
            }
        }
        return exp_body
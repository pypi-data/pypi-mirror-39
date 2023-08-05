# coding=utf-8
from __future__ import print_function
import argparse
import datetime
import time
import json
import logging
import os
import psycopg2
import random  # for generating scoring requests
import requests  # for storing historical MeasurementFacts
from retry import retry
from outdated import warn_if_outdated

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import WatsonMachineLearningInstance, WatsonMachineLearningAsset
from ibm_ai_openscale.supporting_classes import PayloadRecord, Feature
from watson_machine_learning_client import WatsonMachineLearningAPIClient

from src.handle_ssl import *
from src.environments import Environments
from src.setup_env import setup_environment
from src.setup_services_cli import SetupIBMCloudServicesCli
from src.setup_services_rest import SetupIBMCloudServicesRest
from src.utils import jsonFileToDict, getIamHeaders, getExplainabilityBody
from src.version import __version__
from src import logging_temp_file, name

pythonFileDir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)
class AIOSTool(object):

    def __init__(self):
        pass

    def setupWMLModels(self, credentials, env):
        '''
        Discover a list of models in the models sub directory. For each model, create the model in WML,
        Train this model, deploy this model, then configure accuracy monitoring in this model
        '''
        client = WatsonMachineLearningAPIClient(credentials)

        modelInfo = env['heart_drug_model_info']
        myModelName = modelInfo['model_name']
        myDeploymentName = modelInfo['deployment_name']
        myFolderName = modelInfo['folder_name']
        myDeploymentDescription = 'Created by aios fast path.'
        myModelFile = os.path.join(pythonFileDir, 'models', myFolderName, 'model-content.gzip')
        myModelMetaData = os.path.join(pythonFileDir, 'models', myFolderName, 'model-meta.txt')
        myPipelineMetaFile = os.path.join(pythonFileDir, 'models', myFolderName, 'pipeline-meta.json')
        myPipelineFile = os.path.join(pythonFileDir, 'models', myFolderName, 'pipeline-content.tgz')

        logger.info('WML models:')
        client.repository.list_models()

        logger.info('Checking for model named: {}'.format(myModelName))
        models = client.repository.get_model_details()

        for model in models['resources']:
            thisModelName = model['entity']['name']
            if myModelName == thisModelName:
                logger.info('Deleting model: {}'.format(thisModelName))
                client.repository.delete(model['metadata']['guid'])

        logger.info('Creating pipeline for model: {}'.format(myModelName))
        pipelineMetaData = jsonFileToDict(myPipelineMetaFile)
        pipeline_props = {
            client.repository.DefinitionMetaNames.AUTHOR_NAME: pipelineMetaData['author']['name'],
            client.repository.DefinitionMetaNames.NAME: pipelineMetaData['name'],
            client.repository.DefinitionMetaNames.FRAMEWORK_NAME: pipelineMetaData['framework']['name'],
            client.repository.DefinitionMetaNames.FRAMEWORK_VERSION: pipelineMetaData['framework']['version'],
            client.repository.DefinitionMetaNames.RUNTIME_NAME: pipelineMetaData['framework']['runtimes'][0]['name'],
            client.repository.DefinitionMetaNames.RUNTIME_VERSION: pipelineMetaData['framework']['runtimes'][0]['version'],
            client.repository.DefinitionMetaNames.DESCRIPTION: pipelineMetaData['description'],
            client.repository.DefinitionMetaNames.TRAINING_DATA_REFERENCES: pipelineMetaData['training_data_reference']
        }

        client.repository.store_definition(myPipelineFile, meta_props=pipeline_props)

        with open(myModelMetaData) as f:
            metaData = json.load(f)

        model_props = {
            client.repository.ModelMetaNames.NAME: myModelName,
            client.repository.ModelMetaNames.FRAMEWORK_NAME: metaData['framework']['name'],
            client.repository.ModelMetaNames.FRAMEWORK_VERSION: metaData['framework']['version'],
            client.repository.ModelMetaNames.RUNTIME_NAME: metaData['framework']['runtimes'][0]['name'],
            client.repository.ModelMetaNames.RUNTIME_VERSION: metaData['framework']['runtimes'][0]['version'],
            client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: metaData['training_data_reference'][0],
            client.repository.ModelMetaNames.TRAINING_DATA_SCHEMA: {'type': 'struct', 'fields': [{'name': 'AGE', 'nullable': True, 'metadata': {}, 'type': 'double'}, {'name': 'SEX', 'nullable': True, 'metadata': {}, 'type': 'string'}, {'name': 'BP', 'nullable': True, 'metadata': {}, 'type': 'string'}, {'name': 'CHOLESTEROL', 'nullable': True, 'metadata': {}, 'type': 'string'}, {'name': 'NA', 'nullable': True, 'metadata': {}, 'type': 'double'}, {'name': 'K', 'nullable': True, 'metadata': {}, 'type': 'double'}, {'name': 'DRUG', 'nullable': True, 'metadata': {'values': ['drugX', 'drugB', 'drugA', 'drugC'], 'modeling_role': 'target'}, 'type': 'string'}]},
            client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: {'type': 'struct', 'fields': [{'name': 'AGE', 'nullable': True, 'metadata': {}, 'type': 'double'}, {'name': 'SEX', 'nullable': True, 'metadata': {}, 'type': 'string'}, {'name': 'BP', 'nullable': True, 'metadata': {}, 'type': 'string'}, {'name': 'CHOLESTEROL', 'nullable': True, 'metadata': {}, 'type': 'string'}, {'name': 'NA', 'nullable': True, 'metadata': {}, 'type': 'double'}, {'name': 'K', 'nullable': True, 'metadata': {}, 'type': 'double'}, {'name': 'prediction', 'nullable': True, 'metadata': {'modeling_role': 'prediction'}, 'type': 'double'}, {'name': 'predictedLabel', 'nullable': True, 'metadata': {'values': ['drugX', 'drugB', 'drugA', 'drugC'], 'modeling_role': 'decoded-target'}, 'type': 'string'}, {'name': 'probability', 'nullable': True, 'metadata': {'modeling_role': 'probability'}, 'type': {'type': 'array', 'containsNull': True, 'elementType': 'double'}}]},
            client.repository.ModelMetaNames.EVALUATION_METHOD: metaData['evaluation']['method'],
            client.repository.ModelMetaNames.EVALUATION_METRICS: metaData['evaluation']['metrics'],
            client.repository.ModelMetaNames.INPUT_DATA_SCHEMA: {'type': 'struct', 'fields': [{'name': 'AGE', 'nullable': True, 'metadata': {}, 'type': 'double'}, {'name': 'SEX', 'nullable': True, 'metadata': {}, 'type': 'string'}, {'name': 'BP', 'nullable': True, 'metadata': {}, 'type': 'string'}, {'name': 'CHOLESTEROL', 'nullable': True, 'metadata': {}, 'type': 'string'}, {'name': 'NA', 'nullable': True, 'metadata': {}, 'type': 'double'}, {'name': 'K', 'nullable': True, 'metadata': {}, 'type': 'double'}]}
        }

        logger.info('Creating new model')
        details = client.repository.store_model(myModelFile, model_props)
        guid = client.repository.get_model_uid(details)

        logger.info('WML models:')
        client.repository.list_models()

        deploymentDetails = client.deployments.get_details()
        for details in deploymentDetails['resources']:
            depGuid = details['metadata']['guid']
            depName = details['entity']['name']
            logger.info('Name: {}, GUID: {}'.format(depName, depGuid))
            if depName == myDeploymentName:
                try:
                    client.deployments.delete(depGuid)
                except:
                    logger.warning('Error deleting WML deployment: %s', depGuid)

        details = client.deployments.create(artifact_uid=guid, name=myDeploymentName, description=myDeploymentDescription)
        depGuid = details['metadata']['guid']
        depName = details['entity']['name']

        deploymentDetails = client.deployments.get_details()
        for details in deploymentDetails['resources']:
            logger.info('Name: {}, GUID: {}'.format(details['entity']['name'], details['metadata']['guid']))

        return (guid, myModelName, depGuid, depName, metaData)


    @retry(tries=5, delay=4, backoff=2)
    def getAIOSPythonClient(self, aiosCredentials):
        '''
        Connect to AIOS Python client
        '''
        aiosClient = APIClient(aiosCredentials)
        logger.info('Using AI Openscale (AIOS) Python Client version: {}'.format(aiosClient.version))
        return aiosClient

    @retry(tries=5, delay=4, backoff=2)
    def cleanDatamart(self, datamartName, aiosClient):
        logger.info('Clean up datamart, if already present: {}'.format(datamartName))
        subscriptions_uids = aiosClient.data_mart.subscriptions.get_uids()

        # clean up all subscriptions in the datamart
        for subscription_uid in subscriptions_uids:
            # disable explainability, fairness checking, and payload logging for the subscription
            subscription = aiosClient.data_mart.subscriptions.get(subscription_uid)
            subscription.explainability.disable()
            subscription.fairness_monitoring.disable()
            subscription.payload_logging.disable()
            # then remove the subscription itself
            aiosClient.data_mart.subscriptions.delete(subscription_uid)

        # remove bindings
        try:
            bindings_uids = aiosClient.data_mart.bindings.get_uids()
            for binding_uid in bindings_uids:
                aiosClient.data_mart.bindings.delete(binding_uid)
        except:
            logger.warn('datamart bindings could not be deleted')

        # remove previous datamart
        try:
            aiosClient.data_mart.delete()
        except:
            pass # assume datamart doesn't exist, no need to delete

    @retry(tries=5, delay=8, backoff=2)
    def createDatamart(self, datamartName, aiosClient, postgresCredentials):
        '''
        Create datamart schema and datamart
        '''
        self.cleanDatamart(datamartName, aiosClient)

        logger.info('Create datamart: {}'.format(datamartName))

        if postgresCredentials is None:
            aiosClient.data_mart.setup(internal_db=True)
        else:
            hostname = postgresCredentials['uri'].split('@')[1].split(':')[0]
            port = postgresCredentials['uri'].split('@')[1].split(':')[1].split('/')[0]
            user = postgresCredentials['uri'].split('@')[0].split('//')[1].split(':')[0]
            password = postgresCredentials['uri'].split('@')[0].split('//')[1].split(':')[1]
            dbname = postgresCredentials['uri'].split('@')[1].split('/')[1]
            conn_string = "host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(hostname, port, dbname, user, password)
            connection = psycopg2.connect(conn_string)
            # remove previous schema
            with connection:  # transaction
                with connection.cursor() as cursor:
                    cursor.execute('DROP SCHEMA IF EXISTS {} CASCADE'.format(datamartName))
                    cursor.execute('CREATE SCHEMA {}'.format(datamartName))
            aiosClient.data_mart.setup(db_credentials=postgresCredentials, schema=datamartName)
        logger.info('Datamart {} created'.format(datamartName))

    @retry(tries=5, delay=4, backoff=2)
    def bindWMLToAIOS(self, aiosClient, wml_credentials):
        '''
        Bind WML instance to AIOS
        '''
        logger.info('Bind WML instance to AIOS')
        return aiosClient.data_mart.bindings.add('WML instance', WatsonMachineLearningInstance(wml_credentials))

    def registerModelToAIOS(self, modelName, modelGuid, bindingGuid, aiosClient, modelMetaData, datamartName, aiosCredentials, env):
        '''
        Create subscription in AIOS for drug-selection model
        Configure payload logging plus performance, fairness, explainability, and accuracy monitoring
        '''
        subscription = self.addSubscription(modelName, aiosClient, modelGuid)
        self.configureSubscription(modelName, subscription, env, aiosCredentials, modelMetaData, datamartName, modelGuid)

        return subscription

    @retry(tries=5, delay=8, backoff=2)
    def configureSubscription(self, modelName, subscription, env, aiosCredentials, modelMetaData, datamartName, modelGuid):
        logger.info('Enable payload logging in AIOS: {}'.format(modelName))
        subscription.payload_logging.enable()

        logger.info('Enable Performance Monitoring in AIOS: {}'.format(modelName))
        subscription.performance_monitoring.enable()

        if modelName == env['heart_drug_model_info']['model_name']:
            logger.info('Configuring fairness monitoring for model: {}'.format(modelName))
            subscription.fairness_monitoring.enable(
                features=[
                    Feature('AGE', majority=[[49, 59], [60, 75]], minority=[[0, 48], [76, 99]], threshold=0.8),
                    Feature('SEX', majority=['M'], minority=['F'], threshold=0.8)
                ],
                prediction_column='predictedLabel',
                favourable_classes=['drugX', 'drugC'],
                unfavourable_classes=['drugY', 'drugA', 'drugB'],
                min_records=40
            )
        else:
            logger.info('Fairness configuration not yet supported for model: {}'.format(modelName))

        if modelName == env['heart_drug_model_info']['model_name']:
            logger.info('Configuring accuracy monitoring for model: {}'.format(modelName))
            subscription.quality_monitoring.enable(evaluation_method='multiclass', threshold=0.8, min_records=40)
            feedbackValues = [
                [58.0, 'F', 'HIGH', 'NORMAL', 0.868924, 0.061023, 'drugB'],
                [68.0, 'F', 'HIGH', 'NORMAL', 0.77541, 0.0761, 'drugB'],
                [65.0, 'M', 'HIGH', 'NORMAL', 0.635551, 0.056043, 'drugB'],
                [60.0, 'F', 'HIGH', 'HIGH', 0.800607, 0.060181, 'drugB'],
                [70.0, 'M', 'HIGH', 'HIGH', 0.658606, 0.047153, 'drugB'],
                [60.0, 'M', 'HIGH', 'HIGH', 0.805651, 0.057821, 'drugB'],
                [59.0, 'M', 'HIGH', 'HIGH', 0.816356, 0.058583, 'drugB'],
                [72.0, 'M', 'HIGH', 'NORMAL', 0.72142, 0.074552, 'drugB'],
                [53.0, 'F', 'HIGH', 'NORMAL', 0.760809, 0.060889, 'drugB'],
                [55.0, 'F', 'HIGH', 'HIGH', 0.637231, 0.058054, 'drugB'],
                [51.0, 'M', 'HIGH', 'NORMAL', 0.832467, 0.073392, 'drugB'],
                [49.0, 'M', 'HIGH', 'NORMAL', 0.500169, 0.079788, 'drugA'],
                [39.0, 'M', 'HIGH', 'HIGH', 0.731091, 0.075652, 'drugA'],
                [26.0, 'F', 'HIGH', 'NORMAL', 0.781928, 0.063535, 'drugA'],
                [49.0, 'M', 'HIGH', 'NORMAL', 0.538183, 0.061859, 'drugA'],
                [31.0, 'M', 'HIGH', 'NORMAL', 0.749717, 0.06678, 'drugA'],
                [20.0, 'F', 'HIGH', 'HIGH', 0.887426, 0.078798, 'drugA'],
                [42.0, 'M', 'HIGH', 'NORMAL', 0.85794, 0.067203, 'drugA'],
                [48.0, 'M', 'HIGH', 'NORMAL', 0.769197, 0.073633, 'drugA'],
                [47.0, 'M', 'HIGH', 'HIGH', 0.56332, 0.054152, 'drugA'],
                [23.0, 'M', 'HIGH', 'HIGH', 0.53406, 0.066666, 'drugA'],
                [68.0, 'M', 'LOW', 'HIGH', 0.726677, 0.070616, 'drugC'],
                [26.0, 'F', 'LOW', 'HIGH', 0.578002, 0.040819, 'drugC'],
                [32.0, 'F', 'LOW', 'HIGH', 0.730854, 0.075256, 'drugC'],
                [47.0, 'F', 'LOW', 'HIGH', 0.539774, 0.05362, 'drugC'],
                [28.0, 'F', 'LOW', 'HIGH', 0.656292, 0.049997, 'drugC'],
                [22.0, 'M', 'LOW', 'HIGH', 0.526672, 0.064617, 'drugC'],
                [49.0, 'M', 'LOW', 'HIGH', 0.655222, 0.062181, 'drugC'],
                [18.0, 'F', 'NORMAL', 'NORMAL', 0.553567, 0.063265, 'drugX'],
                [49.0, 'M', 'LOW', 'NORMAL', 0.625889, 0.056828, 'drugX'],
                [53.0, 'M', 'NORMAL', 'HIGH', 0.644936, 0.045632, 'drugX'],
                [46.0, 'M', 'NORMAL', 'NORMAL', 0.526226, 0.072234, 'drugX'],
                [39.0, 'M', 'LOW', 'NORMAL', 0.604973, 0.043404, 'drugX'],
                [39.0, 'F', 'NORMAL', 'NORMAL', 0.517515, 0.053301, 'drugX'],
                [15.0, 'M', 'NORMAL', 'HIGH', 0.64236, 0.07071, 'drugX'],
                [23.0, 'M', 'NORMAL', 'HIGH', 0.593596, 0.048417, 'drugX'],
                [50.0, 'F', 'NORMAL', 'NORMAL', 0.601915, 0.048957, 'drugX'],
                [66.0, 'F', 'NORMAL', 'NORMAL', 0.611333, 0.075412, 'drugX'],
                [67.0, 'M', 'NORMAL', 'NORMAL', 0.846892, 0.077711, 'drugX'],
                [60.0, 'M', 'NORMAL', 'NORMAL', 0.645515, 0.063971, 'drugX'],
                [45.0, 'M', 'LOW', 'NORMAL', 0.532632, 0.063636, 'drugX'],
                [17.0, 'M', 'NORMAL', 'NORMAL', 0.722286, 0.06668, 'drugX'],
                [24.0, 'F', 'NORMAL', 'HIGH', 0.80554, 0.07596, 'drugX']
            ]
            feedbackFields = ['AGE', 'SEX', 'BP', 'CHOLESTEROL', 'NA', 'K', 'DRUG']
            subscription.feedback_logging.store(feedbackValues, fields=feedbackFields)
        else:
            logger.info('Accuracy configuration not yet supported for model: {}'.format(modelName))

        if modelName == env['heart_drug_model_info']['model_name']:
            logger.info('Configuring explainability monitoring for model: {}'.format(modelName))
            iamHeaders = getIamHeaders(aiosCredentials, env)
            expBody = getExplainabilityBody(
                modelMetaData,
                datamartName,
                subscription.binding_uid,
                modelGuid,
                ['SEX', 'BP', 'CHOLESTEROL'],
                aiosCredentials
            )
            reply = requests.post(aiosCredentials['url'] + '/v1/model_explanation_configurations', json=expBody, headers=iamHeaders)
            reply.raise_for_status()
        else:
            logger.info('Configuring explainability monitoring for model: {} (not yet supported)'.format(modelName))

    @retry(tries=5, delay=4, backoff=2)
    def addSubscription(self, modelName, aiosClient, modelGuid):
        logger.info('Register WML instance to AIOS: {}'.format(modelName))
        return aiosClient.data_mart.subscriptions.add(WatsonMachineLearningAsset(modelGuid))

    @retry(tries=5, delay=4, backoff=2)
    def reliable_load(self, subscription, recordsList):
        '''
        Retry the loading code so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        return subscription.payload_logging.store(records=recordsList)

    @retry(tries=5, delay=4, backoff=2)
    def reliable_post_metrics(self, metricsurl, iamHeaders, requests, qualityMetric):
        '''
        Retry the loading metrics so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        return requests.post(metricsurl, json=[qualityMetric], headers=iamHeaders)

    def generateSampleScoring(self, datamartName, aiosCredentials, modelName, modelGuid, deployGuid, bindingGuid, subscription, aiosClient, env, args):
        '''
        Generate historical data
        Generate sample scoring requests
        Trigger fairness check
        '''
        metricsurl = '{0}/v1/data_marts/{1}/metrics'.format(aiosCredentials['url'], aiosCredentials['data_mart_id'])
        iamHeaders = getIamHeaders(aiosCredentials, env)

        wmlClient = aiosClient.data_mart.bindings.get_native_engine_client(binding_uid=bindingGuid)
        deploymentDetails = wmlClient.deployments.get_details(deployGuid)
        deploymentUrl = wmlClient.deployments.get_scoring_url(deploymentDetails)

        if modelName == env['heart_drug_model_info']['model_name']:
            logger.info('Load historical scoring records to Payload Logging and MeasurementFacts tables in AIOS: {}'.format(modelName))
            historyfile = os.path.join(pythonFileDir, 'models', env['heart_drug_model_info']['folder_name'], 'historypayloads.json')
        else:
            logger.info('Loading scoring history not yet supported for model: {}'.format(modelName))
            historyfile = None

        historyDays = int(args.history)
        if historyfile != None:
            with open(historyfile) as f:
                payloads = json.load(f)
            for day in range(historyDays):
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
                        'subscription_id': modelGuid,
                        'asset_revision': modelGuid,
                        'deployment_id': deployGuid,
                        'value': {
                            'response_time': score_resp,
                            'records': score_count
                        }
                    }
                    requests.post(metricsurl, json=[performanceMetric], headers=iamHeaders)

        if modelName == env['heart_drug_model_info']['model_name']:
            logger.info('Load historical fairness MeasurementFacts to AIOS: {}'.format(modelName))
            historyfile = os.path.join(pythonFileDir, 'models', env['heart_drug_model_info']['folder_name'], 'historyfairness.json')
        else:
            logger.info('Loading fairness history not yet supported for model: {}'.format(modelName))
            historyfile = None

        if historyfile != None:
            with open(historyfile) as f:
                fairnessValues = json.load(f)
            for day in range(historyDays):
                logger.info('Loading day {}'.format(day+1))
                for hour in range(24):
                    fairnessTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=(-(24*day + hour + 1)))).strftime('%Y-%m-%dT%H:%M:%SZ')
                    fairnessMetric = {
                        'metric_type': 'fairness',
                        'binding_id': bindingGuid,
                        'timestamp': fairnessTime,
                        'subscription_id': modelGuid,
                        'asset_revision': modelGuid,
                        'deployment_id': deployGuid,
                        'value': fairnessValues[random.randint(0, len(fairnessValues))-1]
                    }
                    requests.post(metricsurl, json=[fairnessMetric], headers=iamHeaders)
        else:
            logger.info('Loading fairness history not yet supported for model: {}'.format(modelName))

        logger.info('Load historical quality MeasurementFacts to AIOS: {}'.format(modelName))
        for day in range(historyDays):
            logger.info('Loading day {}'.format(day+1))
            for hour in range(24):
                qualityTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=(-(24*day + hour + 1)))).strftime('%Y-%m-%dT%H:%M:%SZ')
                quality = random.uniform(0.75, 0.95)
                qualityMetric = {
                    'metric_type': 'quality',
                    'binding_id': bindingGuid,
                    'timestamp': qualityTime,
                    'subscription_id': modelGuid,
                    'asset_revision': modelGuid,
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
                self.reliable_post_metrics(metricsurl, iamHeaders, requests, qualityMetric)

        numscores = 100
        logger.info('Generate {} new scoring requests to AIOS: {}'.format(numscores, modelName))
        if modelName == env['heart_drug_model_info']['model_name']:
            for _ in range(numscores):
                scoreInput = {'fields': ['AGE', 'SEX', 'BP', 'CHOLESTEROL', 'NA', 'K'],
                              'values': [[random.randint(15, 80),
                                          random.choice(['F', 'M']),
                                          random.choice(['HIGH', 'LOW', 'NORMAL']),
                                          random.choice(['HIGH', 'NORMAL']),
                                          random.uniform(0.5, 0.9),
                                          random.uniform(0.02, 0.08)]]}
                if args.env == 'icp' and ':31002' not in deploymentUrl:
                    deploymentUrlHost = ':'.join(deploymentUrl.split(':')[:2])
                    argsUrlHost = ':'.join(args.url.split(':')[:2])
                    deploymentUrl = deploymentUrl.replace('{}:16600'.format(deploymentUrlHost), '{}:31002'.format(argsUrlHost))
                wmlClient.deployments.score(deploymentUrl, scoreInput)
        else:
            logger.info('Sample scoring not yet supported for model: {}'.format(modelName))

        logger.info('Trigger immediate fairness check AIOS: {}'.format(modelName))
        subscription.fairness_monitoring.run()
        logger.info('Trigger immediate quality check AIOS: {}'.format(modelName))
        subscription.quality_monitoring.run()


def process_args():
    """Parse the CLI arguments

    Returns:
        dict -- dictionary with the arguments and values
    """

    parser = argparse.ArgumentParser()
    # required parameters
    requiredArgs = parser.add_argument_group('required arguments')
    requiredArgs.add_argument('-a', '--apikey', help='IBM Cloud APIKey', required=True)
    # Optional parameters
    optionalArgs = parser._action_groups.pop()
    parser.add_argument('--env', default='ypprod', help='Environment. Default "ypprod"', choices=['ypprod', 'ypqa', 'ys1dev', 'icp'])
    parser.add_argument('--resource-group', default='default', help='Resource Group to use. If not specified, then "default" group is used')
    parser.add_argument('--organization', help='Cloud Foundry Organization to use', required=False)
    parser.add_argument('--space', help='Cloud Foundry Space to use', required=False)
    parser.add_argument('--postgres', help='Path to postgres credentials file. If not specified, then the internal AIOS database is used')
    parser.add_argument('--wml', help='Path to WML credentials file')
    parser.add_argument('--username', help='ICP username. Required if "icp" environment is chosen')
    parser.add_argument('--password', help='ICP username. Required if "icp" environment is chosen')
    parser.add_argument('--url', help='ICP url. Required if "icp" environment is chosen')
    parser.add_argument('--datamart-name', default='aiosfastpath', help='Specify data mart name, default is "aiosfastpath"')
    parser.add_argument('--history', default=7, help='Days of history to preload. Default is 7', type=int)
    parser.add_argument('--bx', action='store_true', help='Specify (without a value) to use IBM Cloud CLI (bx CLI), default uses Rest API')
    parser.add_argument('--verbose', action='store_true', help='verbose flag')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser._action_groups.append(optionalArgs)
    args = parser.parse_args()

    # validate environment
    if 'throw' in args:
        logger.error(args.throw)
        exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('handle_response').setLevel(logging.DEBUG)
        logging.getLogger('ibm_ai_openscale.utils.client_errors').setLevel(logging.DEBUG)

    warn_if_outdated(name, __version__)

    return args

def main():

    args = process_args()

    def executeMain():
        logger.info('ibm-ai-openscale-cli-{}'.format(__version__))
        logger.info('Log file: {0}'.format(logging_temp_file.name))
        tool = AIOSTool()
        environment = Environments(args).getEnvironment()
        history_days = int(args.history)

        # create the needed service instances and WML  model deployment
        ibm_cloud_services = None
        setup_environment(args, environment)
        if args.bx:
            ibm_cloud_services = SetupIBMCloudServicesCli(args, environment)
        else:
            ibm_cloud_services = SetupIBMCloudServicesRest(args, environment)

        aios_credentials = ibm_cloud_services.setup_aios()
        wml_credentials = ibm_cloud_services.setup_wml()
        postgres_credentials = ibm_cloud_services.setup_postgres_database()

        (modelGuid, modelName, deployGuid, deployName, modelMetaData) = tool.setupWMLModels(wml_credentials, environment)
        logger.info('Model Name: {}  Model GUID: {}'.format(modelName, modelGuid))
        logger.info('Deployment Name: {}  Deployment GUID: {}'.format(deployName, deployGuid))

        datamartName = environment['datamart_name'] if args.datamart_name == 'aiosfastpath' else args.datamart_name

        # Configure the datamart
        aios_client = tool.getAIOSPythonClient(aios_credentials)
        tool.createDatamart(datamartName, aios_client, postgres_credentials)

        wmlBindingGuid = tool.bindWMLToAIOS(aios_client, wml_credentials)
        modelSubscription = tool.registerModelToAIOS(
            modelName,
            modelGuid,
            wmlBindingGuid,
            aios_client,
            modelMetaData,
            datamartName,
            aios_credentials,
            environment)
        tool.generateSampleScoring(
            datamartName,
            aios_credentials,
            modelName,
            modelGuid,
            deployGuid,
            wmlBindingGuid,
            modelSubscription,
            aios_client,
            environment,
            args)

        logger.info('Process completed')
        logger.info('The AI OpenScale dashboard can be accessed at: {}/aiopenscale'.format(environment['aios_url']))

    # until the client supports icp
    if args.env == 'icp':
        with disable_ssl_verification():
            executeMain()
    else:
        executeMain()
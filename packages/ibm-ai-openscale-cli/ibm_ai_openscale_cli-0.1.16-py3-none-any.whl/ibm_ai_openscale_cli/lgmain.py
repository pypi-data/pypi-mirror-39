# coding=utf-8
from __future__ import print_function
import argparse
import datetime
import time
import json
import logging
import os
import random  # for generating scoring requests
import requests  # for storing historical MeasurementFacts
from retry import retry
from outdated import warn_if_outdated
import pandas

from ibm_ai_openscale import APIClient, APIClient4ICP, WatsonMachineLearningInstance4ICP
from ibm_ai_openscale.engines import WatsonMachineLearningInstance, WatsonMachineLearningAsset
from ibm_ai_openscale.supporting_classes import PayloadRecord, Feature
from watson_machine_learning_client import WatsonMachineLearningAPIClient
from ibm_ai_openscale_cli.handle_ssl import *
from ibm_ai_openscale_cli.environments import Environments
from ibm_ai_openscale_cli.setup_env import setup_environment
from ibm_ai_openscale_cli.setup_services_cli import SetupIBMCloudServicesCli
from ibm_ai_openscale_cli.setup_services_rest import SetupIBMCloudServicesRest
from ibm_ai_openscale_cli.utils import jsonFileToDict
from ibm_ai_openscale_cli.version import __version__
from ibm_ai_openscale_cli import logging_temp_file, name
from ibm_ai_openscale_cli.ml_engines.watson_machine_learning.models.drug_selection_model import DrugSelectionModel

pythonFileDir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)
class AIOSTool(object):

    def __init__(self):
        pass

    def setupWMLModels(self, credentials, env, args):
        client = WatsonMachineLearningAPIClient(credentials)

        model = DrugSelectionModel(env).get_metadata()
        modelInfo = model.get_metadata()
        myModelName = modelInfo['model_name']
        myDeploymentName = modelInfo['deployment_name']
        myDeploymentDescription = model['deployment_description']
        myModelFile = model['model_file']
        myModelMetaData = model['model_metadata_file']
        myPipelineMetaFile = model['pipeline_metadata_file']
        myPipelineFile = model['pipeline_file']

        logger.info('Use existing model named: {}'.format(myModelName))
        models = client.repository.get_model_details()

        for model in models['resources']:
            thisModelName = model['entity']['name']
            guid = model['metadata']['guid']
            metaData = model['metadata']
            if myModelName == thisModelName:
                break
        deploymentDetails = client.deployments.get_details()
        for details in deploymentDetails['resources']:
            depGuid = details['metadata']['guid']
            depName = details['entity']['name']
            if depName == myDeploymentName:
                break
        return (guid, myModelName, depGuid, depName, metaData, client)

    @retry(tries=5, delay=4, backoff=2)
    def getAIOSPythonClient(self, aiosCredentials, args):
        '''
        Connect to AIOS Python client
        '''
        aiosClient = None
        if args.env == 'icp':
            aiosClient = APIClient4ICP(aiosCredentials)
        else:
            aiosClient = APIClient(aiosCredentials)
        logger.info('Using AI Openscale (AIOS) Python Client version: {}'.format(aiosClient.version))
        return aiosClient

    def generateScoringRequests(self, wmlClient, modelName, deployGuid, env, args):
        deploymentDetails = wmlClient.deployments.get_details(deployGuid)
        deploymentUrl = wmlClient.deployments.get_scoring_url(deploymentDetails)
        if args.env == 'icp' and ':31002' not in deploymentUrl:
            deploymentUrlHost = ':'.join(deploymentUrl.split(':')[:2])
            argsUrlHost = ':'.join(args.url.split(':')[:2])
            deploymentUrl = deploymentUrl.replace('{}:16600'.format(deploymentUrlHost), '{}:31002'.format(argsUrlHost))

        numscorerequests = args.lg_score_requests
        numscoresperrequest = args.lg_scores_per_request
        pause = args.lg_pause
        perfverbose = args.lg_verbose

        logger.info('Generate {} new scoring requests to AIOS: {}'.format(numscorerequests, modelName))
        totalelapsed = 0
        firststart = datetime.datetime.now()
        lastend = firststart

        for _ in range(numscorerequests):
            scores = []
            for _ in range(numscoresperrequest):
                scores.append([random.randint(15, 80),
                                random.choice(['F', 'M']),
                                random.choice(['HIGH', 'LOW', 'NORMAL']),
                                random.choice(['HIGH', 'NORMAL']),
                                random.uniform(0.5, 0.9),
                                random.uniform(0.02, 0.08)])
            scoreInput = {'fields': ['AGE', 'SEX', 'BP', 'CHOLESTEROL', 'NA', 'K'],
                          'values': scores}
            start = datetime.datetime.now()
            predictions = wmlClient.deployments.score(deploymentUrl, scoreInput)
            end = datetime.datetime.now()
            elapsed = end - start
            elapsed = (elapsed.days*24*3600 + elapsed.seconds) + elapsed.microseconds/1000000.0
            totalelapsed += elapsed
            lastend = end
            if perfverbose:
                logger.info('LG {}: request {} scores(s) in {:.3f} seconds, {} score(s) returned'.format(start, numscoresperrequest, elapsed, len(predictions['values'])))
            if pause > 0.0:
                time.sleep(pause)
        if numscorerequests > 0:
            duration = lastend - firststart
            duration = (duration.days*24*3600 + duration.seconds) + duration.microseconds/1000000.0
            logger.info('LG total score requests: {}, total scores: {}, duration: {:.3f} seconds'.format(numscorerequests, numscorerequests*numscoresperrequest, duration))
            logger.info('LG throughput: {:.3f} score requests per second, {:.3f} scores per second, average score request time: {:.3f} seconds'.format(numscorerequests/duration, numscorerequests*numscoresperrequest/duration, totalelapsed/numscorerequests))

    @retry(tries=5, delay=4, backoff=2)
    def generateOneExplain(self, modelSubscription, scoring_id):
        start = datetime.datetime.now()
        explain = modelSubscription.explainability.run(scoring_id, background_mode=True)
        end = datetime.datetime.now()
        return (start, end, explain)

    def generateExplainRequests(self, modelSubscription, modelName, env, args):

        numexplainrequests = args.lg_explain_requests
        pause = args.lg_pause
        perfverbose = args.lg_verbose

        logger.info('Generate {} explain requests to AIOS: {}'.format(numexplainrequests, modelName))
        scoring_ids = []
        start = datetime.datetime.now()
        payload_table = modelSubscription.payload_logging.get_table_content(format='pandas', limit=args.lg_max_explain_candidates)
        for index, row in payload_table.iterrows():
            scoring_ids.append(row['scoring_id'])
        end = datetime.datetime.now()
        elapsed = end - start
        elapsed = (elapsed.days*24*3600 + elapsed.seconds) + elapsed.microseconds/1000000.0
        if perfverbose:
            logger.info('LG found {} available scores for explain in {:.3f} seconds'.format(len(scoring_ids), elapsed))

        totalelapsed = 0
        firststart = datetime.datetime.now()
        lastend = firststart

        for _ in range(numexplainrequests):
            scoring_id = random.choice(scoring_ids)
            (start, end, explain) = self.generateOneExplain(modelSubscription, scoring_id)
            elapsed = end - start
            elapsed = (elapsed.days*24*3600 + elapsed.seconds) + elapsed.microseconds/1000000.0
            totalelapsed += elapsed
            lastend = end
            if perfverbose:
                logger.info('LG {}: request explain in {:.3f} seconds {} {}'.format(start, elapsed, scoring_id, explain['metadata']['request_id']))
            if pause > 0.0:
                time.sleep(pause)
        if numexplainrequests > 0:
            duration = lastend - firststart
            duration = (duration.days*24*3600 + duration.seconds) + duration.microseconds/1000000.0
            logger.info('LG total explain requests: {}, duration: {:.3f} seconds'.format(numexplainrequests, duration))
            logger.info('LG throughput: {:.3f} explain requests per second, average explain request time: {:.3f} seconds'.format(numexplainrequests/duration, totalelapsed/numexplainrequests))


    def triggerChecks(self, modelName, subscription, args):
        '''
        Trigger fairness and quality checks
        '''
        if args.lg_checks:
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
    parser.add_argument('--db2', help='Path to db2 credentials file')
    parser.add_argument('--wml', help='Path to WML credentials file')
    parser.add_argument('--username', help='ICP username. Required if "icp" environment is chosen')
    parser.add_argument('--password', help='ICP password. Required if "icp" environment is chosen')
    parser.add_argument('--url', help='ICP url. Required if "icp" environment is chosen')
    parser.add_argument('--datamart-name', default='aiosfastpath', help='Specify data mart name, default is "aiosfastpath"')
    parser.add_argument('--bx', action='store_true', help='Specify (without a value) to use IBM Cloud CLI (bx CLI), default uses Rest API')
    parser.add_argument('--verbose', action='store_true', help='verbose flag')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser._action_groups.append(optionalArgs)

    # Optional parameters for LoadGenerator support
    lgArgs = parser._action_groups.pop()
    parser.add_argument('--lg_score_requests', default=0, help='Number of score requests (default = 0)', type=int)
    parser.add_argument('--lg_scores_per_request', default=1, help='Number of scores per score request (default = 1)', type=int)
    parser.add_argument('--lg_explain_requests', default=0, help='Number of explain requests (default = 0)', type=int)
    parser.add_argument('--lg_max_explain_candidates', default=1000, help='Maximum number of candidate scores for explain (default = 1000)', type=int)
    parser.add_argument('--lg_pause', default=0.0, help='Pause in seconds between requests (default = 0.0)', type=float)
    parser.add_argument('--lg_verbose', action='store_true', help='Display individual request response times')
    parser.add_argument('--lg_checks', action='store_true', help='Trigger final fairness and quality checks')
    parser._action_groups.append(lgArgs)

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
        db2_credentials = ibm_cloud_services.setup_db2_database()

        database_credentials = None
        if postgres_credentials is not None:
            database_credentials = postgres_credentials
        if db2_credentials is not None:
            database_credentials = db2_credentials

        (modelGuid, modelName, deployGuid, deployName, modelMetaData, wmlClient) = tool.setupWMLModels(wml_credentials, environment, args)
        logger.info('Model Name: {}  Model GUID: {}'.format(modelName, modelGuid))
        logger.info('Deployment Name: {}  Deployment GUID: {}'.format(deployName, deployGuid))

        datamartName = environment['datamart_name'] if args.datamart_name == 'aiosfastpath' else args.datamart_name
        logger.info('Use existing datamart {}'.format(datamartName))

        aios_client = tool.getAIOSPythonClient(aios_credentials, args)
        wmlBindingGuid = wmlClient.service_instance.get_instance_id()
        modelSubscription = aios_client.data_mart.subscriptions.get(modelGuid)

        tool.generateScoringRequests(wmlClient, modelName, deployGuid, environment, args)
        tool.generateExplainRequests(modelSubscription, modelName, environment, args)
        tool.triggerChecks(modelName, modelSubscription, args)

        logger.info('Process completed')
        logger.info('The AI OpenScale dashboard can be accessed at: {}/aiopenscale'.format(environment['aios_url']))

    # until the client supports icp
    if args.env == 'icp':
        with disable_ssl_verification():
            executeMain()
    else:
        executeMain()

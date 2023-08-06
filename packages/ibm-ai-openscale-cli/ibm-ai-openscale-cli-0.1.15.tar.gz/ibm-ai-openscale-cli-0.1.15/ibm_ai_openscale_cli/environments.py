# coding=utf-8
from __future__ import print_function

class Environments(object):

    def __init__(self, args):
        self.args = args

    def getEnvironment(self):
        return {
            'ypprod': self._getYPProdEnv(),
            'ypqa': self._getYPQAEnv(),
            'ys1dev': self._getYS1DevEnv(),
            'icp': self._getICPEnv()
        }.get(self.args.env)

    def _getYPProdEnv(self):
        attributes = {}
        attributes['name'] = 'YPPROD'
        attributes['api'] = 'https://api.ng.bluemix.net'
        attributes['aios_url'] = 'https://api.aiopenscale.cloud.ibm.com'
        attributes['iam_url'] = 'https://iam.bluemix.net/identity/token'
        attributes['uaa_url'] = 'https://login.ng.bluemix.net/UAALoginServerWAR/oauth/token'
        attributes['resource_controller_url'] = 'https://resource-controller.bluemix.net'
        attributes['resource_group_url'] = 'https://resource-manager.bluemix.net'
        attributes['heart_drug_model_info'] = {}
        attributes['heart_drug_model_info']['model_name'] = 'DrugSelectionModel'
        attributes['heart_drug_model_info']['deployment_name'] = 'DrugSelectionModel'
        attributes['heart_drug_model_info']['folder_name'] = 'DrugSelectionModel'
        attributes['datamart_name'] = 'aiosfastpath'
        return attributes

    def _getYPQAEnv(self):
        attributes = {}
        attributes['name'] = 'YPQA'
        attributes['api'] = 'https://api.ng.bluemix.net'
        attributes['aios_url'] = 'https://api.aiopenscale.test.cloud.ibm.com'
        attributes['iam_url'] = 'https://iam.bluemix.net/identity/token'
        attributes['uaa_url'] = 'https://login.ng.bluemix.net/UAALoginServerWAR/oauth/token'
        attributes['resource_controller_url'] = 'https://resource-controller.bluemix.net'
        attributes['resource_group_url'] = 'https://resource-manager.bluemix.net'
        attributes['heart_drug_model_info'] = {}
        attributes['heart_drug_model_info']['model_name'] = 'DrugSelectionModelYPQA'
        attributes['heart_drug_model_info']['deployment_name'] = 'DrugSelectionModelYPQA'
        attributes['heart_drug_model_info']['folder_name'] = 'DrugSelectionModel'
        attributes['datamart_name'] = 'aiosfastpathypqa'
        return attributes

    def _getYS1DevEnv(self):
        attributes = {}
        attributes['name'] = 'YS1DEV'
        attributes['api'] = 'https://api.stage1.ng.bluemix.net'
        attributes['aios_url'] = 'https://aiopenscale-dev.us-south.containers.appdomain.cloud'
        attributes['iam_url'] = 'https://iam.stage1.bluemix.net/identity/token'
        attributes['uaa_url'] = 'https://login.stage1.ng.bluemix.net/UAALoginServerWAR/oauth/token'
        attributes['resource_controller_url'] = 'https://resource-controller.stage1.bluemix.net'
        attributes['resource_group_url'] = 'https://resource-manager.stage1.bluemix.net'
        attributes['heart_drug_model_info'] = {}
        attributes['heart_drug_model_info']['model_name'] = 'DrugSelectionModelYS1DEV'
        attributes['heart_drug_model_info']['deployment_name'] = 'DrugSelectionModelYS1DEV'
        attributes['heart_drug_model_info']['folder_name'] = 'DrugSelectionModel'
        attributes['datamart_name'] = 'aiosfastpathys1dev'
        return attributes

    def _getICPEnv(self):
        attributes = {}
        attributes['name'] = 'ICP'
        attributes['api'] = None
        attributes['aios_url'] = self.args.url
        attributes['iam_url'] = None
        attributes['uaa_url'] = None
        attributes['resource_controller_url'] = None
        attributes['resource_group_url'] = None
        attributes['heart_drug_model_info'] = {}
        attributes['heart_drug_model_info']['model_name'] = 'DrugSelectionModelICP'
        attributes['heart_drug_model_info']['deployment_name'] = 'DrugSelectionModelICP'
        attributes['heart_drug_model_info']['folder_name'] = 'DrugSelectionModel'
        attributes['datamart_name'] = 'aiosfastpathicp'
        return attributes

# coding=utf-8
from __future__ import print_function
from src.cloud_foundry import CloudFoundry
from src.resource_controller import ResourceController
from src.setup_services import SetupIBMCloudServices
from src.token_manager import TokenManager
from src.utils import jsonFileToDict
import logging

logger = logging.getLogger(__name__)

class SetupIBMCloudServicesRest(SetupIBMCloudServices):

    def __init__(self, args, environment):
        super().__init__(args, environment)
        self.resourceController = None
        self.cloudFoundry = None
        if self.args.env == 'icp':
            return
        iam_access_token = TokenManager(
            apikey=args.apikey,
            url=environment['iam_url']
        ).get_token()
        self.resourceController = ResourceController(
            access_token=iam_access_token,
            url=environment['resource_controller_url'],
            resourceGroupUrl=environment['resource_group_url']
        )
        uaa_access_token = TokenManager(
            apikey=args.apikey,
            url=environment['uaa_url'],
            iam_token=False
        ).get_token()
        self.cloudFoundry = CloudFoundry(access_token=uaa_access_token)

    def _get_credentials(self, params, is_rc_based, credentials_file=None):
        '''
        Returns the credentials from the specified credentials json file. If not
        then returns the credentials an instance of the specified Service.
        If there is no instance available, a new one is provisioned.
        If there are no existing credentials, new one is created and returned.
        '''
        credentials = None

        if credentials_file is not None:
            credentials = self._read_credentials_from_file(credentials_file)
        elif is_rc_based:
            credentials = self.resourceController.get_or_create_instance(
                resource_id=params['resource_id'],
                resource_name=params['instance_name'],
                resource_plan_id=params['resource_plan_id'],
                resource_group_name=self.args.resource_group,
                create_credentials=params['create_credentials']
            )
        elif not is_rc_based:
            credentials = self.cloudFoundry.get_or_create_instance(
                service_name=params['service_name'],
                service_instance_name=params['instance_name'],
                service_plan_guid=params['service_plan_guid'],
                organization_name=self.args.organization,
                space_name=self.args.space
            )
        if ('name' in credentials):
            logger.info('{0} instance: {1}'.format(params['service_display_name'], credentials['name']))
        return credentials

    def setup_aios(self):
        if self.args.env == 'icp':
            return self._aios_icp_credentials()
        aiopenscale_params = {}
        aiopenscale_params['service_display_name'] = 'AI OpenScale'
        aiopenscale_params['instance_name'] = 'aiopenscale-fastpath-instance'
        aiopenscale_params['resource_id'] = '2ad019f3-0fd6-4c25-966d-f3952481a870'
        aiopenscale_params['resource_plan_id'] = '967ba182-c6e0-4adc-92ef-661a822cc1d7' # lite plan
        aiopenscale_params['create_credentials'] = False
        aios_instance = self._get_credentials(aiopenscale_params, True)
        return self._aios_credentials(aios_instance['id'])

    def setup_wml(self):
        wml_params = {}
        wml_params['service_display_name'] = 'Watson Machine Learning'
        if self.args.wml is not None:
            return self._get_credentials(wml_params, None, self.args.wml)
        if self.args.env == 'icp':
            return self._wml_icp_credentials()
        wml_params['instance_name'] = 'wml-fastpath-instance'
        wml_params['resource_id'] = '51c53b72-918f-4869-b834-2d99eb28422a'
        wml_params['resource_plan_id'] = '3f6acf43-ede8-413a-ac69-f8af3bb0cbfe' # lite plan
        wml_params['create_credentials'] = True
        return self._get_credentials(wml_params, True)['credentials']

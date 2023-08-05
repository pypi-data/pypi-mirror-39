# coding=utf-8
from src.utils import jsonFileToDict
import logging

logger = logging.getLogger(__name__)

class SetupIBMCloudServices(object):

    def __init__(self, args, environment):
        self.environment = environment
        self.args = args

    def _read_credentials_from_file(self, credentials_file):
        logger.info('\tCredentials file specified')
        logger.info('\tUsing credentials from "{}"'.format(credentials_file))
        return jsonFileToDict(credentials_file)

    def _aios_credentials(self, data_mart_id):
        aios_credentials = {}
        aios_credentials['apikey'] = self.args.apikey
        aios_credentials['url'] = self.environment['aios_url']
        aios_credentials['data_mart_id'] = data_mart_id
        return aios_credentials

    def _aios_icp_credentials(self):
        logger.info('Setting up {} instance'.format('AI OpenScale'))
        aios_icp_credentials = {}
        aios_icp_credentials['username'] = self.args.username
        aios_icp_credentials['password'] = self.args.password
        aios_icp_credentials['data_mart_id'] = '00000000-0000-0000-0000-000000000000'
        aios_icp_credentials['url'] = '{}'.format(self.args.url)
        aios_icp_credentials['wml_credentials'] = None
        if self.args.wml is not None:
            aios_icp_credentials['wml_credentials'] = self._read_credentials_from_file(self.args.wml)
        return aios_icp_credentials

    def _wml_icp_credentials(self):
        logger.info('Setting up {} instance'.format('Watson Machine Learning'))
        wml_credentials = {}
        wml_credentials['username'] = self.args.username
        wml_credentials['password'] = self.args.password
        wml_credentials['url'] = ':'.join(self.args.url.split(':')[:2])
        wml_credentials['instance_id'] = 'icp'
        wml_credentials['apikey'] = ''
        return wml_credentials

    def setup_postgres_database(self):
        if self.args.postgres is not None:
            logger.info('AIOS PostgreSQL instance: {0} (credentials file)'.format(self.args.postgres))
            return self._read_credentials_from_file(self.args.postgres)
        logger.info('AIOS PostgreSQL instance: internal')
        return None

    def setup_aios(self):
        raise NotImplementedError

    def setup_wml(self):
        raise NotImplementedError
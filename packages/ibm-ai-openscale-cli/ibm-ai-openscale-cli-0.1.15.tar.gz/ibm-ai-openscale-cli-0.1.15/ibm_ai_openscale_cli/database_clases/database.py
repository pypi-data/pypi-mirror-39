# coding=utf-8
import logging

logger = logging.getLogger(__name__)

class Database(object):

    def __init__(self, credentials):
        pass

    def drop_existing_schema(self, schema_name):
        raise NotImplementedError

    def create_new_schema(self, schema_name):
        raise NotImplementedError

    def __del__(self):
        pass
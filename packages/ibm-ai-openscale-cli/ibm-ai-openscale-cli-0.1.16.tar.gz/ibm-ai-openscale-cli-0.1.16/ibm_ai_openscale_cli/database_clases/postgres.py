import psycopg2
from .database import Database
import logging

logger = logging.getLogger(__name__)

DROP_SCHEMA = u'DROP SCHEMA IF EXISTS {} CASCADE'
CREATE_SCHEMA = u'CREATE SCHEMA {}'

class Postgres(Database):

    def __init__(self, credentials):
        super().__init__(credentials)
        hostname = credentials['uri'].split('@')[1].split(':')[0]
        port = credentials['uri'].split('@')[1].split(':')[1].split('/')[0]
        user = credentials['uri'].split('@')[0].split('//')[1].split(':')[0]
        password = credentials['uri'].split('@')[0].split('//')[1].split(':')[1]
        dbname = credentials['uri'].split('@')[1].split('/')[1]
        conn_string = "host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(hostname, port, dbname, user, password)
        self._connection = psycopg2.connect(conn_string)

    def _execute(self, statement_str):
        with self._connection:  # transaction
            with self._connection.cursor() as cursor:
                cursor.execute(statement_str)

    def drop_existing_schema(self, schema_name):
        logger.debug('Dropping schema {}'.format(schema_name))
        self._execute(DROP_SCHEMA.format(schema_name))

    def create_new_schema(self, schema_name):
        logger.debug('Creating schema {}'.format(schema_name))
        self._execute(CREATE_SCHEMA.format(schema_name))
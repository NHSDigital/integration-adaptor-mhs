"""Module containing functionality for a MongoDB implementation of a persistence adaptor."""
import ssl

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

import utilities.integration_adaptors_logger as log
from persistence import persistence_adaptor
from persistence.persistence_adaptor import retriable, RecordCreationError, RecordUpdateError, RecordRetrievalError, \
    RecordDeletionError, validate_data_has_no_primary_key_field, DuplicatePrimaryKeyError
from utilities import config
from utilities.config import config


logger = log.IntegrationAdaptorsLogger(__name__)

_DB_NAME = 'integration-adaptors'
_KEY = "_id"
_CERT_FILE_PATH = "/db-cert.pem"


class MongoPersistenceAdaptor(persistence_adaptor.PersistenceAdaptor):
    """Class responsible for persisting items into a MongoDB."""

    def __init__(self, table_name: str, max_retries: int, retry_delay: float):
        """
        Constructs a MongoDB version of a
        :class:`PersistenceAdaptor <mhs.common.state.persistence_adaptor.PersistenceAdaptor>`.
        The kwargs provided should contain the following information:
          * table_name: The Table Name used to identify the mongo collection containing required items.
          * max_retries: The number of max retries object should make if there is an error connecting with the DB
          * retry_delay: The delay between retries
        :param table_name: Table name to be used in this adaptor.
        """
        self.table_name = table_name
        self.retry_delay = retry_delay
        self.max_retries = max_retries


        cert = config.get_config('DB_CA_CERTS', default=None)
        print(f'Before SSL Check:  cert value is -->{cert} : Typeof cert is {type(cert)}')
        logger.info(f'Before SSL:  cert value is -->{cert} : Typeof cert is {type(cert)}')
        print(config)
        # If cert present create client with ssl enabled
        if cert is not None:
            print(f'SSL Enabled:  cert value is -->{cert} : Typeof cert is {type(cert)}')
            logger.info(f'SSL Enabled:  cert value is -->{cert} : Typeof cert is {type(cert)}')
            cert_file = open(_CERT_FILE_PATH, "a")
            cert_file.write(cert)
            cert_file.close()
            client = AsyncIOMotorClient(
                config.get_config('DB_ENDPOINT_URL'),
                ssl_cert_reqs=ssl.CERT_REQUIRED,
                ssl_ca_certs=_CERT_FILE_PATH
            )
        else:
            client = AsyncIOMotorClient(config.get_config('DB_ENDPOINT_URL'))
        
        self.collection = client[_DB_NAME][table_name]

    @validate_data_has_no_primary_key_field(primary_key=_KEY)
    @retriable
    async def add(self, key: str, data: dict):
        """Add an item to a specified table, using a provided key.

        :param key: The key under which to store the data in persistence.
        :param data: The item to store in persistence.
        """

        logger.info('Adding data for {key} in table {table}', fparams={'key': key, 'table': self.table_name})

        try:
            result = await self.collection.insert_one(self.add_primary_key_field(_KEY, key, data))
            if not result.acknowledged:
                raise RecordCreationError
        except DuplicateKeyError as e:
            raise DuplicatePrimaryKeyError from e
        except Exception as e:
            raise RecordCreationError from e

    @validate_data_has_no_primary_key_field(primary_key=_KEY)
    @retriable
    async def update(self, key: str, data: dict):
        """Updates an item in a specified table, using a provided key.

        :param key: The key used to identify the item.
        :param data: The item to update in persistence.
        :return: The previous version of the item which has been replaced. (None if no previous item)
        """

        logger.info('Updating data for {key} in table {table}', fparams={'key': key, 'table': self.table_name})

        try:
            result = await self.collection.find_one_and_update(
                {_KEY: key},
                {'$set': data},
                return_document=ReturnDocument.AFTER)
            return self.remove_primary_key_field(_KEY, result)
        except Exception as e:
            raise RecordUpdateError from e

    @retriable
    async def get(self, key: str, **kwargs):
        """
        Retrieves an item from a specified table with a given key.
        :param key: The key which identifies the item to get.
        :return: The item from the specified table with the given key. (None if no item found)
        """
        logger.info('Getting record for {key} from table {table}', fparams={'key': key, 'table': self.table_name})
        try:
            result = await self.collection.find_one({_KEY: key})
            return self.remove_primary_key_field(_KEY, result)
        except Exception as e:
            raise RecordRetrievalError from e

    @retriable
    async def delete(self, key):
        """
        Removes an item from a table given it's key.
        :param key: The key of the item to delete.
        :return: The instance of the item which has been deleted from persistence. (None if no item found)
        """
        logger.info('Deleting record for {key} from table {table}', fparams={'key': key, 'table': self.table_name})
        try:
            result = await self.collection.find_one_and_delete({_KEY: key})
            return self.remove_primary_key_field(_KEY, result)
        except Exception as e:
            raise RecordDeletionError from e

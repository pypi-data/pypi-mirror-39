import os
import subprocess

import yaml
import pymongo

from biomap.core.database import BioMapDB
from biomap.backend.mongodb.mapper import MongoDBMapper

def create_dir_if_it_does_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

class BioMapMongoDB(BioMapDB):

    tmp_files = os.path.expanduser('~/.biomap/tmp')

    def __init__(self, host='localhost', port=27017, **kwargs):
        create_dir_if_it_does_not_exist(self.tmp_files)
        self.client = pymongo.MongoClient(host=host, port=port, **kwargs)
        # THE database
        self.db = self.client.biomap
        # mapper definitions
        self._mappers = self.db.mappers

    @staticmethod
    def read_configuration_file(path):
        with open(path, 'r') as conf:
            return yaml.load(conf)

    def _get_mapper_definition(self, mapper_name):
        return self.db.mappers.find_one( {'name': mapper_name} )

    def mapper_exists(self, mapper_name):
        return bool(self._mappers.find_one({'name': mapper_name}))

    def mapper_data_exists(self, data_name):
        return data_name in self.db.collection_names()

    @property
    def mapper_data(self):
        return {doc['mapper_data'] for doc in self._mappers.find()}

    def _create_mapper(self, definition, data):
        '''

        '''
        self.__insert_mapper_data(definition.mapper_data, data)
        self.__insert_mapper_definition(definition)

    def __insert_mapper_definition(self, definition):
        '''

        '''
        self._mappers.insert_one(definition)

    def __insert_mapper_data(self, data_name, mapper_data):
        '''

        '''
        collection = self.db.create_collection(data_name)
        return collection.insert_many(mapper_data)

    def _define_mapper(self, mapper_definition):
        self.__insert_mapper_definition(mapper_definition)

    def _get_mapper_data(self, mapper_name):
        return list(self.db.get_collection(mapper_name).find())

    def get_mapper(self, mapper_name):
        if not self.mapper_exists(mapper_name):
            raise LookupError("Mapper '{}' does not exists."
                              .format(mapper_name))
        return MongoDBMapper(mapper_name, self)

    @property
    def mappers(self):
        return [mapper['name'] for mapper in self._mappers.find()]

    def delete_mapper(self, mapper_name):
        self._mappers.delete_one({'name': mapper_name})

    def _delete_mapper_data(self, data_name, cascade):
        if cascade:
            self._mappers.delete_many({'mapper_data': data_name})
        self.db.get_collection(mapper_data).drop()

    def _purge_mapper(self, mapper_name, cascade):
        data_name = self.get_mapper_definition(mapper_name)
        self.delete_mapper(mapper_name)
        self.delete_mapper_data(data_name, cascade)

    def _update_mapper(self, mapper_name, mapper_data):
        data_name = self._mappers.find_one({'name': mapper_name})['mapper_data']
        self.delete_mapper_data(data_name, False)
        self.__insert_mapper_data(data_name, mapper_data)

    def get_mappers(self, data_name):
        return {doc['name'] for doc in self._mappers.find({'mapper_data': data_name})}

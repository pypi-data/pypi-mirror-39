'''

'''
import os
import yaml

CONFIG = {}
CONN_CONFIG=os.environ.get('BIOMAP_CONN_CONFIG')
if CONN_CONFIG is not None:
    CONFIG = yaml.load(CONN_CONFIG)

BACKEND = os.environ.get('BIOMAP_BACKEND', 'mongo')

class BioMap:
    def __init__(self, backend=BACKEND, config=CONFIG):
        self.db = self.get_backend(backend, config)

    @classmethod
    def get_backend(cls, backend, config):
        biomap_db = None
        if backend == 'mongo':
            from biomap.backends.mongodb.database import BioMapMongoDB
            biomap_db = BioMapMongoDB(**config)
        elif backend == 'postgres':
            from biomap.backends.postgres.database import BioMapPostgres
            biomap_db = BioMapPostgres(**config)
        return biomap_db

    def get_mapper(self, mapper_name):
        return self.db.get_mapper(mapper_name)

    def __call__(self, mapper_name):
        return self.get_mapper(mapper_name)

    @property
    def database(self):
        return self.db

    @property
    def mappers(self):
        return self.db.mappers

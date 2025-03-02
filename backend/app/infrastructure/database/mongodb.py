from pymongo import MongoClient
from pymongo.database import Database

from app.infrastructure.environment_configs import EnvironmentConfigs

env = EnvironmentConfigs()


class MongoDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDatabase, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.value = MongoClient(env.mongo_uri)[env.mongo_db]
            self._initialized = True

    def get_database(self) -> Database:
        return self.value

import os
from typing import Optional


class EnvironmentConfigs:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvironmentConfigs, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._mongo_uri = os.environ.get(
                "MONGO_URI", "mongodb://dbuser:dbpassword@db:27017/"
            )
            self._mongo_db = os.environ.get("MONGO_DB", "db")
            self._aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
            self._aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
            self._region_name = os.environ.get("AWS_REGION", "us-east-1")
            self._aws_local_endpoint = os.environ.get("AWS_LOCAL_ENDPOINT", None)
            self._product_images_bucket_name = os.environ.get(
                "PRODUCT_IMAGES_BUCKET_NAME", ""
            )

            self._initialized = True

    @property
    def mongo_uri(self) -> str:
        return self._mongo_uri

    @property
    def mongo_db(self) -> str:
        return self._mongo_db

    @property
    def aws_access_key_id(self) -> str:
        return self._aws_access_key_id

    @property
    def aws_secret_access_key(self) -> str:
        return self._aws_secret_access_key

    @property
    def region_name(self) -> str:
        return self._region_name

    @property
    def aws_local_endpoint(self) -> Optional[str]:
        return self._aws_local_endpoint

    @property
    def product_images_bucket_name(self) -> str:
        return self._product_images_bucket_name

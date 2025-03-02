import boto3

from app.application.file_storage import BaseFileStorage
from app.application.schemas.image_file import File
from app.infrastructure.environment_configs import EnvironmentConfigs

env = EnvironmentConfigs()


class S3FileStorage(BaseFileStorage):
    def __init__(
        self,
        bucket_name: str,
    ):
        self.bucket_name = bucket_name
        self.region_name = env.region_name

        extra_args = {}

        if env.aws_local_endpoint:
            extra_args["endpoint_url"] = env.aws_local_endpoint

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=env.aws_access_key_id,
            aws_secret_access_key=env.aws_secret_access_key,
            region_name=env.region_name,
            **extra_args,
        )

    async def put(self, key: str, file: File) -> str:
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=file.content,
            ACL="public-read",
            ContentType=file.content_type,
        )

        return self.__get_file_url(key)

    def __get_file_url(self, key: str) -> str:
        if env.aws_local_endpoint:
            return f"{env.aws_local_endpoint.replace('localstack', '127.0.0.1')}/{self.bucket_name}/{key}"

        return f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{key}"

    async def delete(self, key: str):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)

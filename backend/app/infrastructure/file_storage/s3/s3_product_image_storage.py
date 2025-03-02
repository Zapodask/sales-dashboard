from app.application.file_storage.product_image_storage import ProductImageFileStorage
from app.infrastructure.environment_configs import EnvironmentConfigs
from . import S3FileStorage


env = EnvironmentConfigs()


class S3ProductImageFileStorage(ProductImageFileStorage, S3FileStorage):
    def __init__(self):
        super().__init__(bucket_name=env.product_images_bucket_name)

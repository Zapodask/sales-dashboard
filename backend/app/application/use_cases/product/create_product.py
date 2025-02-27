from typing import List
from uuid import uuid4
from app.application.file_storage.product_image_storage import ProductImageFileStorage
from app.application.schemas.product import ProductCreateSchema
from app.domain.entities.product import Product
from app.domain.exceptions.not_found_exception import NotFoundException
from app.application.repositories.product_repository import ProductRepository
from app.application.repositories.category_repository import CategoryRepository


class CreateProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
        product_image_storage: ProductImageFileStorage,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.product_image_storage = product_image_storage

    async def execute(self, product_input: ProductCreateSchema) -> Product:
        await self.__check_categories_existence(product_input.category_ids)

        product_id = str(uuid4())

        image_url = await self.product_image_storage.put(
            product_id, product_input.image
        )

        product = Product(
            id=product_id,
            name=product_input.name,
            description=product_input.description,
            price=product_input.price,
            category_ids=product_input.category_ids,
            image_url=image_url,
        )

        return await self.product_repository.create(product)

    async def __check_categories_existence(self, category_ids: List[str]) -> None:
        category_ids_len = len(category_ids)
        if category_ids_len == 0:
            return

        existing_categories = await self.category_repository.get_existing_ids(
            category_ids
        )

        if category_ids_len != len(existing_categories):
            categories_not_found = [
                category_id
                for category_id in category_ids
                if category_id not in existing_categories
            ]
            raise NotFoundException(
                f"Categories with ids {categories_not_found} does not exist"
            )

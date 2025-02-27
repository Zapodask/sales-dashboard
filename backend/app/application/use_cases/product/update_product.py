from typing import List
from app.application.file_storage.product_image_storage import ProductImageFileStorage
from app.application.schemas.product import ProductUpdateSchema
from app.domain.entities.product import Product
from app.domain.exceptions.not_found_exception import NotFoundException
from app.application.repositories.product_repository import ProductRepository
from app.application.repositories.category_repository import CategoryRepository


class UpdateProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
        product_image_storage: ProductImageFileStorage,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.product_image_storage = product_image_storage

    async def execute(
        self, product_id: str, product_input: ProductUpdateSchema
    ) -> Product:
        product = await self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundException(f"Product with id {product_id} does not exist")

        await self.__update_fields(product, product_input)

        return await self.product_repository.update(product)

    async def __update_fields(
        self, product: Product, product_input: ProductUpdateSchema
    ) -> None:
        if product_input.name:
            product.name = product_input.name

        if product_input.description:
            product.description = product_input.description

        if product_input.price:
            product.price = product_input.price

        if product_input.category_ids:
            await self.__check_categories_existence(product_input.category_ids)
            product.category_ids = product_input.category_ids

        if product_input.image:
            product.image_url = await self.product_image_storage.put(
                product.id, product_input.image
            )

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

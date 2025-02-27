from app.application.repositories.category_repository import CategoryRepository
from app.application.repositories.product_repository import ProductRepository


class DeleteCategoryUseCase:
    def __init__(
        self,
        category_repository: CategoryRepository,
        product_repository: ProductRepository,
    ):
        self.category_repository = category_repository
        self.product_repository = product_repository

    async def execute(self, category_id: str) -> None:
        category_products = await self.product_repository.get_by_category(category_id)

        if len(category_products) > 0:
            for product in category_products:
                product.category_ids.remove(category_id)

            await self.product_repository.bulk_update(category_products)

        await self.category_repository.delete(category_id)

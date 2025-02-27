from typing import List
from app.domain.entities.product import Product
from app.application.repositories.product_repository import ProductRepository


class GetAllProductsUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self) -> List[Product]:
        return await self.product_repository.get_all()

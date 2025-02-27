from typing import Optional
from app.domain.entities.product import Product
from app.application.repositories.product_repository import ProductRepository


class GetProductByIdUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, product_id: str) -> Optional[Product]:
        return await self.product_repository.get_by_id(product_id)

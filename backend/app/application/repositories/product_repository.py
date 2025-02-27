from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def bulk_update(self, products: List[Product]) -> List[Product]:
        pass

    @abstractmethod
    async def delete(self, product_id: str) -> bool:
        pass

    @abstractmethod
    async def get_by_category(self, category_id: str) -> List[Product]:
        pass

    @abstractmethod
    async def get_existing_ids(self, product_ids: List[str]) -> List[str]:
        pass

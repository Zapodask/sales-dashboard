from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def get_by_id(self, category_id: str) -> Optional[Category]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Category]:
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def delete(self, category_id: str) -> bool:
        pass

    @abstractmethod
    async def get_existing_ids(self, category_ids: List[str]) -> List[str]:
        pass

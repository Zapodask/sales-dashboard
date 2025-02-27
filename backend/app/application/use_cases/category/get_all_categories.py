from typing import List
from app.domain.entities.category import Category
from app.application.repositories.category_repository import CategoryRepository


class GetAllCategoriesUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def execute(self) -> List[Category]:
        return await self.category_repository.get_all()

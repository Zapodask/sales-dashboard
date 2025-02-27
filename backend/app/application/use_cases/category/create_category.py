from uuid import uuid4
from app.application.schemas.category import CategoryCreateSchema
from app.domain.entities.category import Category
from app.application.repositories.category_repository import CategoryRepository


class CreateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def execute(self, category_input: CategoryCreateSchema) -> Category:
        category = Category(id=str(uuid4()), name=category_input.name)
        return await self.category_repository.create(category)

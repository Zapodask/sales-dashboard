from app.application.schemas.category import CategoryUpdateSchema
from app.domain.entities.category import Category
from app.domain.exceptions.not_found_exception import NotFoundException
from app.application.repositories.category_repository import CategoryRepository


class UpdateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def execute(
        self, category_id: str, category_input: CategoryUpdateSchema
    ) -> Category:
        category = await self.category_repository.get_by_id(category_id)

        if category is None:
            raise NotFoundException(f"Category with id {category_id} does not exist")

        if category_input.name:
            category.name = category_input.name

        return await self.category_repository.update(category)

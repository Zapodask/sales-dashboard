from app.domain.entities.category import Category
from app.domain.exceptions.not_found_exception import NotFoundException
from app.application.repositories.category_repository import CategoryRepository


class GetCategoryByIdUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def execute(self, category_id: str) -> Category:
        category = await self.category_repository.get_by_id(category_id)

        if category is None:
            raise NotFoundException(f"Category with id {category_id} does not exist")

        return category

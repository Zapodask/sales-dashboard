from fastapi import APIRouter, Depends, status

from app.application.repositories.category_repository import CategoryRepository
from app.application.repositories.product_repository import ProductRepository
from app.application.schemas.category import CategoryCreateSchema, CategoryUpdateSchema
from app.application.use_cases.category.create_category import CreateCategoryUseCase
from app.application.use_cases.category.delete_category import DeleteCategoryUseCase
from app.application.use_cases.category.get_all_categories import (
    GetAllCategoriesUseCase,
)
from app.application.use_cases.category.get_category_by_id import GetCategoryByIdUseCase
from app.application.use_cases.category.update_category import UpdateCategoryUseCase
from app.infrastructure.database.mongodb import MongoDatabase
from app.infrastructure.repositories.mongodb.mongodb_category_repository import (
    MongodbCategoryRepository,
)
from app.infrastructure.repositories.mongodb.mongodb_product_repository import (
    MongodbProductRepository,
)


category_router = APIRouter(prefix="/categories")

mongo_db = MongoDatabase()


def get_category_repository() -> CategoryRepository:
    return MongodbCategoryRepository(mongo_db.get_database())


def get_product_repository() -> ProductRepository:
    return MongodbProductRepository(mongo_db.get_database())


@category_router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreateSchema,
    category_repository: CategoryRepository = Depends(get_category_repository),
):
    use_case = CreateCategoryUseCase(category_repository)

    return await use_case.execute(category_data)


@category_router.get("")
async def get_categories(
    category_repository: CategoryRepository = Depends(get_category_repository),
):
    use_case = GetAllCategoriesUseCase(category_repository)

    return await use_case.execute()


@category_router.get("/{category_id}")
async def get_category_by_id(
    category_id: str,
    category_repository: CategoryRepository = Depends(get_category_repository),
):
    use_case = GetCategoryByIdUseCase(category_repository)

    return await use_case.execute(category_id)


@category_router.patch("/{category_id}")
async def update_category(
    category_id: str,
    category_data: CategoryUpdateSchema,
    category_repository: CategoryRepository = Depends(get_category_repository),
):
    use_case = UpdateCategoryUseCase(category_repository)

    return await use_case.execute(category_id, category_data)


@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    category_repository: CategoryRepository = Depends(get_category_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
):
    use_case = DeleteCategoryUseCase(category_repository, product_repository)

    await use_case.execute(category_id)

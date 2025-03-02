import json
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.application.file_storage.product_image_storage import ProductImageFileStorage
from app.application.repositories.category_repository import CategoryRepository
from app.application.repositories.order_repository import OrderRepository
from app.application.repositories.product_repository import ProductRepository
from app.application.schemas.image_file import File as DomainFile
from app.application.schemas.product import (
    ProductCreateSchema,
    ProductUpdateSchema,
)
from app.application.use_cases.product.create_product import CreateProductUseCase
from app.application.use_cases.product.delete_product import DeleteProductUseCase
from app.application.use_cases.product.get_all_products import GetAllProductsUseCase
from app.application.use_cases.product.get_product_by_id import GetProductByIdUseCase
from app.application.use_cases.product.update_product import UpdateProductUseCase
from app.infrastructure.database.mongodb import MongoDatabase
from app.infrastructure.file_storage.s3.s3_product_image_storage import (
    S3ProductImageFileStorage,
)
from app.infrastructure.repositories.mongodb.mongodb_category_repository import (
    MongodbCategoryRepository,
)
from app.infrastructure.repositories.mongodb.mongodb_order_repository import (
    MongodbOrderRepository,
)
from app.infrastructure.repositories.mongodb.mongodb_product_repository import (
    MongodbProductRepository,
)

product_router = APIRouter(prefix="/products")

mongo_db = MongoDatabase()


def get_product_repository() -> ProductRepository:
    return MongodbProductRepository(mongo_db.get_database())


def get_category_repository() -> CategoryRepository:
    return MongodbCategoryRepository(mongo_db.get_database())


def get_order_repository() -> OrderRepository:
    return MongodbOrderRepository(mongo_db.get_database())


def get_image_file_storage() -> ProductImageFileStorage:
    return S3ProductImageFileStorage()


@product_router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_ids: str = Form(...),
    image: UploadFile = File(...),
    product_repository: ProductRepository = Depends(get_product_repository),
    category_repository: CategoryRepository = Depends(get_category_repository),
    image_file_storage: ProductImageFileStorage = Depends(get_image_file_storage),
):
    use_case = CreateProductUseCase(
        product_repository, category_repository, image_file_storage
    )

    create_schema = ProductCreateSchema(
        name=name,
        description=description,
        price=price,
        category_ids=json.loads(category_ids),
        image=DomainFile(
            content=await image.read(),
            content_type=image.content_type,
        ),
    )

    return await use_case.execute(create_schema)


@product_router.get("")
async def get_products(
    product_repository: ProductRepository = Depends(get_product_repository),
):
    use_case = GetAllProductsUseCase(product_repository)

    return await use_case.execute()


@product_router.get("/{product_id}")
async def get_product_by_id(
    product_id: str,
    product_repository: ProductRepository = Depends(get_product_repository),
):
    use_case = GetProductByIdUseCase(product_repository)

    return await use_case.execute(product_id)


@product_router.patch("/{product_id}")
async def update_product(
    product_id: str,
    name: Optional[str] = Form(...),
    description: Optional[str] = Form(...),
    price: Optional[float] = Form(...),
    category_ids: Optional[str] = Form(...),
    image: UploadFile | None = None,
    product_repository: ProductRepository = Depends(get_product_repository),
    category_repository: CategoryRepository = Depends(get_category_repository),
    image_file_storage: ProductImageFileStorage = Depends(get_image_file_storage),
):
    use_case = UpdateProductUseCase(
        product_repository, category_repository, image_file_storage
    )

    update_schema = ProductUpdateSchema(
        name=name,
        description=description,
        price=price,
        category_ids=json.loads(category_ids) if category_ids else None,
        image=(
            DomainFile(content=await image.read(), content_type=image.content_type)
            if image
            else None
        ),
    )

    return await use_case.execute(product_id, update_schema)


@product_router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    product_repository: ProductRepository = Depends(get_product_repository),
    order_repository: OrderRepository = Depends(get_order_repository),
    image_file_storage: ProductImageFileStorage = Depends(get_image_file_storage),
):
    use_case = DeleteProductUseCase(
        product_repository, order_repository, image_file_storage
    )

    await use_case.execute(product_id)

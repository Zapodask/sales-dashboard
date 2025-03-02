from fastapi import APIRouter, Depends, status

from app.application.repositories.order_repository import OrderRepository
from app.application.repositories.product_repository import ProductRepository
from app.application.schemas.order import OrderCreateSchema, OrderUpdateSchema
from app.application.use_cases.order.create_order import CreateOrderUseCase
from app.application.use_cases.order.delete_order import DeleteOrderUseCase
from app.application.use_cases.order.get_all_orders import GetallOrdersUseCase
from app.application.use_cases.order.get_order_by_id import GetOrderByIdUseCase
from app.application.use_cases.order.update_order import UpdateOrderUseCase
from app.infrastructure.database.mongodb import MongoDatabase
from app.infrastructure.repositories.mongodb.mongodb_order_repository import (
    MongodbOrderRepository,
)
from app.infrastructure.repositories.mongodb.mongodb_product_repository import (
    MongodbProductRepository,
)


order_router = APIRouter(prefix="/orders")

mongo_db = MongoDatabase()


def get_order_repository() -> OrderRepository:
    return MongodbOrderRepository(mongo_db.get_database())


def get_product_repository() -> ProductRepository:
    return MongodbProductRepository(mongo_db.get_database())


@order_router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreateSchema,
    order_repository: OrderRepository = Depends(get_order_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
):
    use_case = CreateOrderUseCase(order_repository, product_repository)

    return await use_case.execute(order_data)


@order_router.get("")
async def get_orders(
    order_repository: OrderRepository = Depends(get_order_repository),
):
    use_case = GetallOrdersUseCase(order_repository)

    return await use_case.execute()


@order_router.get("/{order_id}")
async def get_order_by_id(
    order_id: str,
    order_repository: OrderRepository = Depends(get_order_repository),
):
    use_case = GetOrderByIdUseCase(order_repository)

    return await use_case.execute(order_id)


@order_router.patch("/{order_id}")
async def update_order(
    order_id: str,
    order_data: OrderUpdateSchema,
    order_repository: OrderRepository = Depends(get_order_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
):
    use_case = UpdateOrderUseCase(order_repository, product_repository)

    return await use_case.execute(order_id, order_data)


@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: str,
    order_repository: OrderRepository = Depends(get_order_repository),
):
    use_case = DeleteOrderUseCase(order_repository)

    await use_case.execute(order_id)

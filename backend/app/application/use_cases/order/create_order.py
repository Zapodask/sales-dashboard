from typing import List
from uuid import uuid4
from app.application.schemas.order import OrderCreateSchema
from app.domain.entities.order import Order
from app.domain.exceptions.not_found_exception import NotFoundException
from app.application.repositories.order_repository import OrderRepository
from app.application.repositories.product_repository import ProductRepository


class CreateOrderUseCase:
    def __init__(
        self, order_repository: OrderRepository, product_repository: ProductRepository
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository

    async def execute(self, order_input: OrderCreateSchema) -> Order:
        await self.__check_products_existence(order_input.product_ids)

        order = Order(
            id=str(uuid4()),
            date=order_input.date,
            product_ids=order_input.product_ids,
            total=order_input.total,
        )

        return await self.order_repository.create(order)

    async def __check_products_existence(self, product_ids: List) -> None:
        products_len = len(product_ids)
        if products_len == 0:
            return

        existing_products = await self.product_repository.get_existing_ids(product_ids)

        if products_len != len(existing_products):
            products_not_found = [
                product_id
                for product_id in product_ids
                if product_id not in existing_products
            ]
            raise NotFoundException(
                f"Products with ids {products_not_found} does not exist"
            )

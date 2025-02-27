from typing import List
from app.application.schemas.order import OrderUpdateSchema
from app.domain.entities.order import Order
from app.domain.exceptions.not_found_exception import NotFoundException
from app.application.repositories.order_repository import OrderRepository
from app.application.repositories.product_repository import ProductRepository


class UpdateOrderUseCase:
    def __init__(
        self, order_repository: OrderRepository, product_repository: ProductRepository
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository

    async def execute(self, order_id: str, order_input: OrderUpdateSchema) -> Order:
        order = await self.order_repository.get_by_id(order_id)

        if order is None:
            raise NotFoundException(f"Order with id {order_id} does not exist")

        await self.__update_fields(order, order_input)

        return await self.order_repository.update(order)

    async def __update_fields(
        self, order: Order, order_input: OrderUpdateSchema
    ) -> Order:
        if order_input.date:
            order.date = order_input.date

        if order_input.total:
            order.total = order_input.total

        if order_input.product_ids:
            await self.__check_products_existence(order_input.product_ids)
            order.product_ids = order_input.product_ids

        return order

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

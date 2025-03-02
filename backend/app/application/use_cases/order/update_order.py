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

        if order_input.product_ids:
            total = await self.__get_total(order_input.product_ids)
            order.product_ids = order_input.product_ids
            order.total = total

        return order

    async def __get_total(self, product_ids: List) -> float:
        products_len = len(product_ids)

        products_prices = await self.product_repository.get_prices(product_ids)
        existing_products = [id for id, _ in products_prices]

        if products_len != len(products_prices):
            products_not_found = [
                product_id
                for product_id in product_ids
                if product_id not in existing_products
            ]
            raise NotFoundException(
                f"Products with ids {products_not_found} does not exist"
            )

        return round(sum([price for _, price in products_prices]), 2)

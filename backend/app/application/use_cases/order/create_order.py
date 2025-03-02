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
        total = await self.__get_total(order_input.product_ids)

        order = Order(
            id=str(uuid4()),
            date=order_input.date,
            product_ids=order_input.product_ids,
            total=total,
        )

        return await self.order_repository.create(order)

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

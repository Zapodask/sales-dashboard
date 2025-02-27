from typing import List
from app.domain.entities.order import Order
from app.application.repositories.order_repository import OrderRepository


class GetallOrdersUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self) -> List[Order]:
        return await self.order_repository.get_all()

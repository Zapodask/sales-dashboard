from app.domain.entities.order import Order
from app.domain.exceptions.not_found_exception import NotFoundException
from app.application.repositories.order_repository import OrderRepository


class GetOrderByIdUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, order_id: str) -> Order:
        order = await self.order_repository.get_by_id(order_id)

        if order is None:
            raise NotFoundException(f"Order with id {order_id} does not exist")

        return order

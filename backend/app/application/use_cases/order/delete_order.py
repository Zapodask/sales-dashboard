from app.application.repositories.order_repository import OrderRepository


class DeleteOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, order_id: str) -> None:
        await self.order_repository.delete(order_id)

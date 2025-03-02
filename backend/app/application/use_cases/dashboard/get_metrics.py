from datetime import date
from typing import Optional
from app.application.repositories.order_repository import OrderRepository
from app.application.schemas.dashboard import DashboardMetricsSchema


class GetMetricsUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(
        self,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> DashboardMetricsSchema:
        return await self.order_repository.get_metrics(
            start_date=start_date,
            end_date=end_date,
        )

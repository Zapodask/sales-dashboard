from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from app.application.schemas.dashboard import DashboardMetricsSchema
from app.domain.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Order]:
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def bulk_update(self, orders: List[Order]) -> List[Order]:
        pass

    @abstractmethod
    async def delete(self, order_id: str) -> None:
        pass

    @abstractmethod
    async def get_by_product(self, product_id: str) -> List[Order]:
        pass

    @abstractmethod
    async def get_metrics(
        self, start_date: Optional[date], end_date: Optional[date]
    ) -> DashboardMetricsSchema:
        pass

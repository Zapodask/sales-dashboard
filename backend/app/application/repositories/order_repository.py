from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

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
    async def delete(self, order_id: str) -> bool:
        pass

    @abstractmethod
    async def get_by_product(self, product_id: str) -> List[Order]:
        pass

    @abstractmethod
    async def get_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Order]:
        pass

    @abstractmethod
    async def get_aggregated_data(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        pass

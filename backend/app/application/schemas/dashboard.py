from typing import List

from pydantic import BaseModel


class DashboardMetricsSchema(BaseModel):
    total_orders: int
    average_order_value: float
    total_revenue: float
    orders_by_period: dict
    top_products: List[dict]
    revenue_by_category: List[dict]

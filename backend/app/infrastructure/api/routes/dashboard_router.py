from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.application.repositories.order_repository import OrderRepository
from app.application.use_cases.dashboard.get_metrics import GetMetricsUseCase
from app.infrastructure.database.mongodb import MongoDatabase
from app.infrastructure.repositories.mongodb.mongodb_order_repository import (
    MongodbOrderRepository,
)


dashboard_router = APIRouter(prefix="/dashboard")

mongo_db = MongoDatabase()


def get_order_repository() -> OrderRepository:
    return MongodbOrderRepository(mongo_db.get_database())


@dashboard_router.get("")
async def get_metrics(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    order_repository: OrderRepository = Depends(get_order_repository),
):
    use_case = GetMetricsUseCase(order_repository)

    return await use_case.execute(start_date, end_date)

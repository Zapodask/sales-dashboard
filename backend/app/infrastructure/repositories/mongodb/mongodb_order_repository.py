from datetime import date, datetime
from typing import List, Optional
from pymongo import UpdateOne
from pymongo.database import Database

from app.application.repositories.order_repository import OrderRepository
from app.application.schemas.dashboard import DashboardMetricsSchema
from app.domain.entities.order import Order


class MongodbOrderRepository(OrderRepository):
    def __init__(self, db: Database):
        self.db = db
        self.orders_collection = self.db["orders"]

    async def create(self, order: Order) -> Order:
        db_order = {
            "_id": order.id,
            "total": order.total,
            "date": order.date,
            "product_ids": order.product_ids,
        }

        self.orders_collection.insert_one(db_order)

        return order

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        db_order = self.orders_collection.find_one({"_id": order_id})

        if db_order is None:
            return

        return Order(
            id=db_order["_id"],
            total=db_order["total"],
            date=db_order["date"],
            product_ids=db_order["product_ids"],
        )

    async def get_all(self) -> List[Order]:
        db_orders = self.orders_collection.find()

        return [
            Order(
                id=db_order["_id"],
                total=db_order["total"],
                date=db_order["date"],
                product_ids=db_order["product_ids"],
            )
            for db_order in db_orders
        ]

    async def update(self, order: Order) -> Order:
        db_order = {
            "total": order.total,
            "date": order.date,
            "product_ids": order.product_ids,
        }

        self.orders_collection.update_one({"_id": order.id}, {"$set": db_order})

        return order

    async def bulk_update(self, orders: List[Order]) -> List[Order]:
        operations = [
            UpdateOne(
                {"_id": order.id},
                {
                    "$set": {
                        "total": order.total,
                        "date": order.date,
                        "product_ids": order.product_ids,
                    }
                },
            )
            for order in orders
        ]

        self.orders_collection.bulk_write(operations)

        return orders

    async def delete(self, order_id: str) -> None:
        self.orders_collection.delete_one({"_id": order_id})

    async def get_by_product(self, product_id: str) -> List[Order]:
        db_orders = self.orders_collection.find({"product_ids": {"$in": [product_id]}})

        return [
            Order(
                id=db_order["_id"],
                total=db_order["total"],
                date=db_order["date"],
                product_ids=db_order["product_ids"],
            )
            for db_order in db_orders
        ]

    async def get_metrics(
        self,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> DashboardMetricsSchema:
        filter_query = {}

        start_datetime = (
            datetime.combine(start_date, datetime.min.time()) if start_date else None
        )
        end_datetime = (
            datetime.combine(end_date, datetime.max.time()) if end_date else None
        )

        if start_datetime and end_datetime:
            filter_query = {"date": {"$gte": start_datetime, "$lte": end_datetime}}
        elif start_datetime:
            filter_query = {"date": {"$gte": start_datetime}}
        elif end_datetime:
            filter_query = {"date": {"$lte": end_datetime}}

        total_orders = self.orders_collection.count_documents(filter_query)

        pipeline_revenue = [
            {"$match": filter_query},
            {
                "$group": {
                    "_id": None,
                    "total_revenue": {"$sum": "$total"},
                    "avg_order": {"$avg": "$total"},
                }
            },
        ]
        revenue_results = self.orders_collection.aggregate(pipeline_revenue).to_list(1)
        total_revenue = 0
        average_order_value = 0

        if revenue_results:
            total_revenue = revenue_results[0].get("total_revenue", 0)
            average_order_value = revenue_results[0].get("avg_order", 0)

        pipeline_by_period = [
            {"$match": filter_query},
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
                    "count": {"$sum": 1},
                    "revenue": {"$sum": "$total"},
                }
            },
            {"$sort": {"_id": 1}},
        ]
        orders_by_period_results = self.orders_collection.aggregate(
            pipeline_by_period
        ).to_list(None)
        orders_by_period = {
            item["_id"]: {"count": item["count"], "revenue": item["revenue"]}
            for item in orders_by_period_results
        }

        pipeline_top_products = [
            {"$match": filter_query},
            {"$unwind": "$product_ids"},
            {"$group": {"_id": "$product_ids", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5},
            {
                "$lookup": {
                    "from": "products",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "product_info",
                }
            },
            {"$unwind": "$product_info"},
            {
                "$project": {
                    "product_name": "$product_info.name",
                    "product_id": "$_id",
                    "count": 1,
                }
            },
        ]
        top_products = self.orders_collection.aggregate(pipeline_top_products).to_list(
            None
        )

        pipeline_revenue_by_category = [
            {"$match": filter_query},
            {"$unwind": "$product_ids"},
            {
                "$lookup": {
                    "from": "products",
                    "localField": "product_ids",
                    "foreignField": "_id",
                    "as": "product",
                }
            },
            {"$unwind": "$product"},
            {"$unwind": "$product.category_ids"},
            {
                "$group": {
                    "_id": "$product.category_ids",
                    "revenue": {"$sum": "$product.price"},
                }
            },
            {
                "$lookup": {
                    "from": "categories",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "category",
                }
            },
            {"$unwind": "$category"},
            {
                "$project": {
                    "category_name": "$category.name",
                    "category_id": "$_id",
                    "revenue": 1,
                }
            },
            {"$sort": {"revenue": -1}},
        ]

        revenue_by_category = self.orders_collection.aggregate(
            pipeline_revenue_by_category
        ).to_list(None)

        return DashboardMetricsSchema(
            total_orders=total_orders,
            average_order_value=average_order_value,
            total_revenue=total_revenue,
            orders_by_period=orders_by_period,
            top_products=top_products,
            revenue_by_category=revenue_by_category,
        )

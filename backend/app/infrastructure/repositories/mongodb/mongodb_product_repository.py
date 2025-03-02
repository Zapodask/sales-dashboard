from typing import List, Optional, Tuple
from pymongo import UpdateOne
from pymongo.database import Database

from app.application.repositories.product_repository import ProductRepository
from app.domain.entities.product import Product


class MongodbProductRepository(ProductRepository):
    def __init__(self, db: Database):
        self.db = db
        self.products_collection = self.db["products"]

    async def create(self, product: Product) -> Product:
        db_product = {
            "_id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_ids": product.category_ids,
            "image_url": product.image_url,
        }

        self.products_collection.insert_one(db_product)

        return product

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        db_product = self.products_collection.find_one({"_id": product_id})

        if db_product is None:
            return

        return Product(
            id=db_product["_id"],
            name=db_product["name"],
            description=db_product["description"],
            price=db_product["price"],
            category_ids=db_product["category_ids"],
            image_url=db_product["image_url"],
        )

    async def get_all(self) -> List[Product]:
        db_products = self.products_collection.find()

        return [
            Product(
                id=db_product["_id"],
                name=db_product["name"],
                description=db_product["description"],
                price=db_product["price"],
                category_ids=db_product["category_ids"],
                image_url=db_product["image_url"],
            )
            for db_product in db_products
        ]

    async def update(self, product: Product) -> Product:
        db_product = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_ids": product.category_ids,
            "image_url": product.image_url,
        }

        self.products_collection.update_one({"_id": product.id}, {"$set": db_product})

        return product

    async def bulk_update(self, products: List[Product]) -> List[Product]:
        operations = []

        for product in products:
            product_id = product.id

            db_product = {
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category_ids": product.category_ids,
                "image_url": product.image_url,
            }

            operations.append(UpdateOne({"_id": product_id}, {"$set": db_product}))

        self.products_collection.bulk_write(operations)

        return products

    async def delete(self, product_id: str) -> None:
        db_product_orders = self.db["orders"].find(
            {"product_ids": {"$in": [product_id]}}
        )

        operations = []

        for order in db_product_orders:
            order.product_ids.remove(product_id)
            operations.append(UpdateOne({"_id": order["_id"]}, {"$set": order}))

        if len(operations) > 0:
            self.db["orders"].bulk_write(operations)

        self.products_collection.delete_one({"_id": product_id})

    async def get_by_category(self, category_id: str) -> List[Product]:
        db_products = self.products_collection.find(
            {"category_ids": {"$in": [category_id]}}
        )

        return [
            Product(
                id=db_product["_id"],
                name=db_product["name"],
                description=db_product["description"],
                price=db_product["price"],
                category_ids=db_product["category_ids"],
                image_url=db_product["image_url"],
            )
            for db_product in db_products
        ]

    async def get_prices(self, product_ids: List[str]) -> List[Tuple[str, float]]:
        db_products = self.products_collection.find({"_id": {"$in": product_ids}})

        return [(db_product["_id"], db_product["price"]) for db_product in db_products]

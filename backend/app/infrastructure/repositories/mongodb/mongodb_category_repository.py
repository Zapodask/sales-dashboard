from typing import List, Optional
from pymongo.database import Database
from pymongo.operations import UpdateOne

from app.application.repositories.category_repository import CategoryRepository
from app.domain.entities.category import Category


class MongodbCategoryRepository(CategoryRepository):
    def __init__(self, db: Database):
        self.db = db
        self.categories_collection = self.db["categories"]

    async def create(self, category: Category) -> Category:
        db_category = {
            "_id": category.id,
            "name": category.name,
        }

        self.categories_collection.insert_one(db_category)

        return category

    async def get_by_id(self, category_id: str) -> Optional[Category]:
        db_category = self.categories_collection.find_one({"_id": category_id})

        if db_category is None:
            return

        return Category(
            id=db_category["_id"],
            name=db_category["name"],
        )

    async def get_all(self) -> List[Category]:
        db_categories = self.categories_collection.find()

        return [
            Category(
                id=db_category["_id"],
                name=db_category["name"],
            )
            for db_category in db_categories
        ]

    async def update(self, category: Category) -> Category:
        db_category = {
            "name": category.name,
        }

        self.categories_collection.update_one(
            {"_id": category.id}, {"$set": db_category}
        )

        return category

    async def delete(self, category_id: str) -> None:
        db_category_products = self.db["products"].find(
            {"category_id": {"$in": [category_id]}}
        )

        operations = []

        for product in db_category_products:
            product.category_ids.remove(category_id)
            operations.append(UpdateOne({"_id": product["_id"]}, {"$set": product}))

        if len(operations) > 0:
            self.db["products"].bulk_write(operations)

        self.categories_collection.delete_one({"_id": category_id})

    async def get_existing_ids(self, category_ids: List[str]) -> List[str]:
        db_categories = self.categories_collection.find({"_id": {"$in": category_ids}})

        return [db_category["_id"] for db_category in db_categories]

import typer
import random
from faker import Faker
from pymongo import MongoClient
from bson.objectid import ObjectId

from app.infrastructure.environment_configs import EnvironmentConfigs

fake = Faker()
app = typer.Typer()
env = EnvironmentConfigs()

client = MongoClient(env.mongo_uri)
db = client[env.mongo_db]
categories_collection = db["categories"]
products_collection = db["products"]
orders_collection = db["orders"]


def generate_categories(n=5):
    categories = []
    for _ in range(n):
        category = {"_id": str(ObjectId()), "name": fake.word().capitalize()}
        categories.append(category)
    categories_collection.insert_many(categories)
    return categories


def generate_products(n=20, categories=[]):
    products = []
    for _ in range(n):
        category_ids = random.sample(
            [c["_id"] for c in categories], k=random.randint(1, 2)
        )
        product = {
            "_id": str(ObjectId()),
            "name": fake.word().capitalize(),
            "description": fake.sentence(),
            "price": round(random.uniform(5, 500), 2),
            "category_ids": category_ids,
            "image_url": fake.image_url(),
        }
        products.append(product)
    products_collection.insert_many(products)
    return products


def generate_orders(n=10, products=[]):
    orders = []
    for _ in range(n):
        selected_products = random.sample(products, k=random.randint(1, 5))
        product_ids = [p["_id"] for p in selected_products]
        total = sum(p["price"] for p in selected_products)
        order = {
            "_id": str(ObjectId()),
            "date": fake.date_time_between(start_date="-1y", end_date="now"),
            "product_ids": product_ids,
            "total": round(total, 2),
        }
        orders.append(order)
    orders_collection.insert_many(orders)
    return orders


@app.command()
def populate_db(categories: int = 5, products: int = 20, orders: int = 10):
    typer.echo("Generating categories...")
    cats = generate_categories(categories)
    typer.echo("Generating products...")
    prods = generate_products(products, cats)
    typer.echo("Generating orders...")
    generate_orders(orders, prods)
    typer.echo("Database successfully populated!")


if __name__ == "__main__":
    app()

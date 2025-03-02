from typing import List
from dataclasses import dataclass


@dataclass
class Product:
    id: str
    name: str
    description: str
    price: float
    category_ids: List[str]
    image_url: str

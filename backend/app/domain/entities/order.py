from typing import List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    id: str
    product_ids: List[str]
    total: float
    date: datetime

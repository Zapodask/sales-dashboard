from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class OrderBaseSchema(BaseModel):
    product_ids: List[str] = Field(...)
    total: float = Field(..., gt=0)
    date: datetime = Field(default_factory=datetime.now)


class OrderCreateSchema(OrderBaseSchema):
    pass


class OrderUpdateSchema(BaseModel):
    product_ids: Optional[List[str]] = None
    total: Optional[float] = Field(None, gt=0)
    date: Optional[datetime] = None

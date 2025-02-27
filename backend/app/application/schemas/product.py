from typing import List, Optional
from pydantic import BaseModel, Field


class ProductBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category_ids: List[str] = Field(...)


class ProductCreateSchema(ProductBaseSchema):
    image: bytes = Field(...)


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    category_ids: Optional[List[str]] = None
    image: Optional[bytes] = None

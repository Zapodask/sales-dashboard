from typing import Optional
from pydantic import BaseModel, Field


class CategoryBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryCreateSchema(CategoryBaseSchema):
    pass


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)

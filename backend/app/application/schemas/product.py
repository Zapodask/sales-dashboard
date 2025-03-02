from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.application.schemas.image_file import File


class ProductBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    price: float = Field(...)
    category_ids: List[str] = Field(...)


class ProductCreateSchema(ProductBaseSchema):
    image: File

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ProductUpdateWithoutImageSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    category_ids: Optional[List[str]] = None


class ProductUpdateSchema(ProductUpdateWithoutImageSchema):
    image: Optional[File] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

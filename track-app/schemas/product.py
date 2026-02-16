from pydantic import BaseModel, Field
from datetime import date

class ProductCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    image_url: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class ProductResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float
    image_url: str
    description: str
    created_at: date

    class Config:
        from_attributes = True

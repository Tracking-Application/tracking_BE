from pydantic import BaseModel
from datetime import datetime


# Create Order
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    address: str
    city: str
    state: str


# Response Schema
class OrderResponse(BaseModel):
    id: int
    product_title: str
    quantity: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# Update Status (Admin)
class OrderStatusUpdate(BaseModel):
    status: str

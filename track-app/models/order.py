from sqlalchemy import Column, Integer, String, Float, Text, Date, ForeignKey, DateTime
from models.base import Base
from datetime import date
from sqlalchemy.sql import func


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity = Column(Integer, default=1, nullable=False)
    total_price = Column(Float, default=0)

    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)

    status = Column(String(50), default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
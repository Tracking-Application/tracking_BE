from sqlalchemy import Column, Integer, String, Float, Text, Date, ForeignKey, DateTime
from models.base import Base
from datetime import date


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(Date, default=date.today)







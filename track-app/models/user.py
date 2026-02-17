import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.sql import func
from datetime import datetime, date

class RoleEnum(str, enum.Enum):
    admin = "admin"
    customer = "customer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)

    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(Date, default=date.today)  

import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), default="user", nullable=False)  # user/admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

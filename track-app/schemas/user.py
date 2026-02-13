# schemas/user.py
from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    # password: constr(min_length=6, max_length=128)


class AdminRegister(BaseModel):
    full_name: str
    email: EmailStr
    # password: constr(min_length=6, max_length=128)
    password: str
    admin_secret: str


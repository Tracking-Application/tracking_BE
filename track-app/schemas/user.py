# schemas/user.py
from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str


class AdminRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    admin_secret: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UpdateUserProfile(BaseModel):
    name: str
    phone: str

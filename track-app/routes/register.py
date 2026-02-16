
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_session
from models.user import User, RoleEnum
from schemas.user import UserRegister,AdminRegister
from utils.passwd import hash_password

router = APIRouter()

# ===============================
## User Register
# ===============================

# @router.post("/register/user", tags=["User"])
# async def register_user(
#     user_data: UserRegister,
#     db: AsyncSession = Depends(get_session)
# ):

#     result = await db.execute(
#         select(User).where(User.email == user_data.email)
#     )
#     if result.scalar_one_or_none():
#         raise HTTPException(status_code=400, detail="Email already registered")

#     new_user = User(
#         full_name=user_data.full_name,
#         email=user_data.email,
#         phone=user_data.phone,
#         password_hash=hash_password(user_data.password),
#         role="user"
#     )

#     db.add(new_user)
#     await db.commit()

#     return {"message": "User registered successfully"}

@router.post("/register/user", tags=["User"])
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role=RoleEnum.customer
    )

    db.add(new_user)
    await db.commit()

    return {"message": "User registered successfully"}


# ===============================
## Admin Register
# ===============================

ADMIN_SECRET = "#12345"

# @router.post("/register/admin", tags=["Admin"])
# async def register_admin(
#     admin_data: AdminRegister,
#     db: AsyncSession = Depends(get_session)
# ):

#     # Validate admin secret
#     if admin_data.admin_secret != ADMIN_SECRET:
#         raise HTTPException(status_code=400, detail="Invalid admin secret")

#     # Check if email already exists
#     result = await db.execute(
#         select(User).where(User.email == admin_data.email)
#     )
#     if result.scalar_one_or_none():
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Create admin
#     new_admin = User(
#         full_name=admin_data.full_name,
#         email=admin_data.email,
#         password_hash=hash_password(admin_data.password),
#         role="admin"
#     )

#     db.add(new_admin)
#     await db.commit()

#     return {"message": "Admin registered successfully"}

@router.post("/register/admin", tags=["Admin"])
async def register_admin(
    admin_data: AdminRegister,
    db: AsyncSession = Depends(get_session)
):
    

    result = await db.execute(
        select(User).where(User.email == admin_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if admin_data.admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=400, detail="Invalid admin secret")

    new_admin = User(
        name=admin_data.name,
        email=admin_data.email,
        password_hash=hash_password(admin_data.password),
        role=RoleEnum.admin
    )

    db.add(new_admin)
    await db.commit()

    return {"message": "Admin registered successfully"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_session
from models.user import User, RoleEnum
from schemas.user import UserRegister, AdminRegister, UpdateUserProfile
from utils.passwd import hash_password

router = APIRouter()

# ===============================
## User Register
# ===============================

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


@router.get("/user/profile/{user_id}", tags=["User"])
async def get_user_profile(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Optional: prevent admin from accessing this API
    if user.role != RoleEnum.customer:
        raise HTTPException(status_code=403, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role.value,
        "created_at": user.created_at
    }


@router.put("/user/profile/{user_id}", tags=["User"])
async def update_user_profile(
    user_id: int,
    updated_data: UpdateUserProfile,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Only allow customer to update
    if user.role != RoleEnum.customer:
        raise HTTPException(status_code=403, detail="Access denied")

    # Update fields
    user.name = updated_data.name
    user.phone = updated_data.phone

    await db.commit()
    await db.refresh(user)

    return {
        "message": "Profile updated successfully",
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone
    }

@router.get("/all/users", tags=["User"])
async def get_all_customers(
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(User).where(User.role == RoleEnum.customer)
    )
    users = result.scalars().all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "created_at": user.created_at
        }
        for user in users
    ]


# ===============================
## Admin Register
# ===============================

ADMIN_SECRET = "#12345"

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

from sqlalchemy import func

@router.get("/users/count", tags=["Admin"])
async def get_total_customers(
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(func.count())
        .select_from(User)
        .where(User.role == RoleEnum.customer)
    )

    total_users = result.scalar()

    return {
        "total_customers": total_users
    }

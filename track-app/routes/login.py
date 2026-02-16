from fastapi import Request, APIRouter, Depends, HTTPException
from schemas.user import LoginSchema
from sqlalchemy.ext.asyncio import AsyncSession
from utils.passwd import verify_password
from sqlalchemy import select
from database.db import get_session
from models.user import User


router = APIRouter()

@router.post("/login",tags=["Login"])
async def login_user(
    login_data: LoginSchema,
    db: AsyncSession = Depends(get_session)
):

    # Check email exists
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "name"   : user.name,
        "role": user.role
    }


# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

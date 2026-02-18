from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_session

from models.order import Order
from models.product import Product
from models.user import User

from schemas.order import OrderCreate, OrderStatusUpdate
#router = APIRouter(prefix="/orders", tags=["Orders"])
router = APIRouter()

#CREATE ORDER (USER)

@router.post("/orders/create", tags=["Orders"])
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_session)
):

    # Check user exists
    result = await db.execute(
        select(User).where(User.id == order_data.user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != "customer":
        raise HTTPException(status_code=403, detail="Only users can place orders")

    # Check product exists
    result = await db.execute(
        select(Product).where(Product.id == order_data.product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Calculate total
    total = product.price * order_data.quantity

    new_order = Order(
        user_id=order_data.user_id,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_price=total,
        address=order_data.address,
        city=order_data.city,
        state=order_data.state
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    return {
        "message": "Order placed successfully",
        "order_id": new_order.id
    }


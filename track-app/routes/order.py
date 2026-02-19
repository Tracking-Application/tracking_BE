from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_session
from sqlalchemy.sql import func
from models.order import Order
from models.product import Product
from models.user import User

from schemas.order import OrderCreate, OrderStatusUpdate
#router = APIRouter(prefix="/orders", tags=["Orders"])
router = APIRouter()

###############################################################################
#CREATE ORDER (USER)
###############################################################################

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

###############################################################################
# GET MY ORDERS (USER PAGE)
###############################################################################

@router.get("/my-orders/{user_id}", tags=["Orders"])
async def get_my_orders(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Order, Product.title)
        .join(Product, Order.product_id == Product.id)
        .where(Order.user_id == user_id)
    )

    orders = []

    for order, title in result.all():
        orders.append({
            "id": order.id,
            "product_title": title,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "status": order.status,
            "created_at": order.created_at
        })

    return orders

###############################################################################
# ADMIN – GET ALL ORDERS
###############################################################################

@router.get("/admin/order/{admin_id}", tags=["Orders"])
async def get_all_orders(
    admin_id: int,
    db: AsyncSession = Depends(get_session)
):

    # Verify admin
    result = await db.execute(
        select(User).where(User.id == admin_id)
    )
    admin = result.scalar_one_or_none()

    if not admin or admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(
        select(Order, Product.title, User.name)
        .join(Product, Order.product_id == Product.id)
        .join(User, Order.user_id == User.id)
    )

    data = []

    for order, product_title, user_name in result.all():
        data.append({
            "order_id": order.id,
            "customer": user_name,
            "product": product_title,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "status": order.status
        })

    return data

###############################################################################
# ADMIN – UPDATE ORDER STATUS
###############################################################################

@router.put("/{admin_id}/update-status/{order_id}", tags=["Orders"])
async def update_order_status(
    admin_id: int,
    order_id: int,
    status_data: OrderStatusUpdate,
    db: AsyncSession = Depends(get_session)
):

    # Check admin
    result = await db.execute(
        select(User).where(User.id == admin_id)
    )
    admin = result.scalar_one_or_none()

    if not admin or admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status_data.status

    await db.commit()

    return {"message": "Order status updated successfully"}

###############################################################################
# ADMIN – GET TOTAL ORDER 
###############################################################################

@router.get("/total_order/{admin_id}",tags=["Order-Details"])
async def admin_total_orders(
    admin_id: int,
    db: AsyncSession = Depends(get_session)
):

    # Verify admin
    result = await db.execute(
        select(User).where(User.id == admin_id)
    )
    admin = result.scalar_one_or_none()

    if not admin or admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(
        select(func.count(Order.id))
    )

    total = result.scalar()

    return {
        "total_orders": total
    }

###############################################################################
# ADMIN – Total Orders by DELIVERED
###############################################################################

@router.get("/total/delivered", tags=["Order-Details"])
async def total_delivered_orders(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(func.count(Order.id))
        .where(Order.status == "Delivered")
    )

    total = result.scalar()

    return {"total_delivered": total}

###############################################################################
# ADMIN – Total Orders by PENDING
###############################################################################

@router.get("/total/pending", tags=["Order-Details"])
async def total_pending_orders(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(func.count(Order.id))
        .where(Order.status == "Pending")
    )

    total = result.scalar()

    return {"total_pending": total}

###############################################################################
# ADMIN – Total Orders by SHIPPING
###############################################################################

@router.get("/total/shipping", tags=["Order-Details"])
async def total_pending_orders(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(func.count(Order.id))
        .where(Order.status == "Shipping")
    )

    total = result.scalar()

    return {"total_shipping": total}

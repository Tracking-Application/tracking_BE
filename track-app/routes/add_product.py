from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_session
from models.product import Product
from schemas.product import ProductResponse, ProductCreate
# from uploads

router = APIRouter()

import os
import shutil
from fastapi import UploadFile, File, Form

UPLOAD_FOLDER = "uploads"

@router.post("/add-product",tags=["Product"])
async def add_product(
    title: str = Form(...),
    author: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    # Create uploads folder if not exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Save image file
    file_path = os.path.join(UPLOAD_FOLDER, image.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Save product in DB
    new_product = Product(
        title=title,
        author=author,
        price=price,
        image_url=file_path,
        description=description
    )

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return {
        "message": "Product added successfully",
        "id": new_product.id,
        "title": new_product.title,
        "image_url": new_product.image_url
    }


# @router.post("/admin/add-product", response_model=ProductResponse, tags=["Product"])
# async def add_product(
#     product_data: ProductCreate,
#     db: AsyncSession = Depends(get_session)
# ):
#     new_product = Product(
#         title=product_data.title,
#         author=product_data.author,
#         price=product_data.price,
#         image_url=product_data.image_url,
#         description=product_data.description
#     )

#     db.add(new_product)
#     await db.commit()
#     await db.refresh(new_product)

#     return new_product

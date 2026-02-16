from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_session
from models.product import Product
from schemas.product import ProductResponse, ProductCreate
# from uploads

router = APIRouter()

import os, shutil, uuid
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


@router.get("/get-product", tags=["Product"])
async def get_all_products(
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(Product))
    products = result.scalars().all()

    return [
        {
            "id": product.id,
            "title": product.title,
            "author": product.author,
            "price": product.price,
            "description": product.description,
            "image_url": f"http://localhost:8000/{product.image_url}",
            "created_at": product.created_at
        }
        for product in products
    ]

@router.get("/product/{product_id}", tags=["Product"])
async def get_single_product(
    product_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": product.id,
        "title": product.title,
        "author": product.author,
        "price": product.price,
        "description": product.description,
        "image_url": f"http://localhost:8000/{product.image_url}",
        "created_at": product.created_at
    }


UPLOAD_FOLDER = "uploads"

@router.put("/update-product/{product_id}", tags=["Product"])
async def update_product(
    product_id: int,
    title: str = Form(...),
    author: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    image: UploadFile = File(None),  # optional image
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update basic fields
    product.title = title
    product.author = author
    product.price = price
    product.description = description

    # If new image uploaded
    if image:
        # Delete old image file
        if os.path.exists(product.image_url):
            os.remove(product.image_url)

        # Save new image
        unique_filename = f"{uuid.uuid4()}_{image.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        product.image_url = file_path

    await db.commit()
    await db.refresh(product)

    return {
        "message": "Product updated successfully",
        "id": product.id,
        "image_url": f"http://localhost:8000/{product.image_url}"
    }

@router.delete("/delete-product/{product_id}", tags=["Product"])
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Delete image file
    if os.path.exists(product.image_url):
        os.remove(product.image_url)

    # Delete product from DB
    await db.delete(product)
    await db.commit()

    return {"message": "Product deleted successfully"}

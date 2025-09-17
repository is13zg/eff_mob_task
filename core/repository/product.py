from models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Sequence


async def create_product_in_db(new_product: Product, db: AsyncSession) -> Product:
    db.add(new_product)
    return new_product


async def get_all_products_from_db(db: AsyncSession) -> Sequence[Product]:
    res = await db.execute(select(Product))
    products = res.scalars().all()
    return products


async def get_own_products_from_db(db: AsyncSession, user_id: int) -> Sequence[Product]:
    res = await db.execute(select(Product).where(Product.owner_id == user_id))
    products = res.scalars().all()
    return products


async def get_product_from_db(prod_id: int, db: AsyncSession) -> Product:
    res = await db.execute(select(Product).where(Product.id == prod_id))
    return res.scalar_one_or_none()


async def update_product_in_db(data: dict, prod_id: int, db: AsyncSession) -> Product:
    res = await db.execute(update(Product).where(Product.id == prod_id).values(**data).returning(Product))
    return res.scalar_one_or_none()


async def delete_product_from_db(product_id: int, db: AsyncSession) -> None:
    await db.execute(delete(Product).where(Product.id == product_id))




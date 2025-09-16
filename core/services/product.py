from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.product import ProductIn, ProductOut, ProductUpdate
from models.product import Product
from core.repository.product import create_product_in_db, get_all_products_from_db, get_own_products_from_db, \
    get_product_from_db, update_product_in_db, delete_product_from_db
from typing import List


async def create_product(user: User, data: ProductIn, db: AsyncSession) -> ProductOut:
    new_product = Product(name=data.name, owner_id=user.id, count=data.count, price=data.price)
    db_product = await create_product_in_db(new_product, db)
    await db.commit()
    await db.refresh(db_product)
    return ProductOut.from_orm(db_product)


async def update_product(data: dict, prod_id: int, db: AsyncSession) -> ProductOut:
    db_product = await update_product_in_db(data, prod_id, db)
    await db.commit()
    return ProductOut.from_orm(db_product)


async def get_all_products(db: AsyncSession) -> List[ProductOut]:
    res = await get_all_products_from_db(db)
    return [ProductOut.from_orm(prod) for prod in res]


async def get_own_products(db: AsyncSession, user_id: int) -> List[ProductOut]:
    res = await get_own_products_from_db(db, user_id)
    return [ProductOut.from_orm(prod) for prod in res]


async def get_prod_by_id(prod_id: int, db: AsyncSession) -> Product:
    res = await get_product_from_db(prod_id, db)
    return res


async def delete_product(product_id: int, db: AsyncSession) -> None:
    await delete_product_from_db(product_id, db)
    await db.commit()

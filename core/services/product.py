from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.product import ProductIn, ProductOut
from models.product import Product
from core.repository.product import create_product_in_db


async def create_product(user: User, data: ProductIn, db: AsyncSession) -> Product:
    new_product = Product(name=data.name, owner_id=user.id, count=data.count, price=data.price)
    db_product = await create_product_in_db(new_product, db)
    await db.commit()
    await db.refresh(db_product)
    return db_product

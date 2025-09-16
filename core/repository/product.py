from models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession


async def create_product_in_db(new_product: Product, db: AsyncSession) -> Product:
    db.add(new_product)
    return new_product

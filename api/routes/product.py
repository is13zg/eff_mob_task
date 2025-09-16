from fastapi import APIRouter, Depends
from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.services.user import auth_user
from models.user import User
from schemas.product import ProductIn, ProductOut
from core.permisions import check_permission
from core.services.product import create_product
from typing import Tuple

product_router = APIRouter(prefix="/products", tags=["Work with products", ])

ELEMENT_NAME = "products"


@product_router.post("/")
async def create(
        data: ProductIn, auth: Tuple[User, str] = Depends(auth_user), db: AsyncSession = Depends(get_session),
) -> ProductOut:
    user, jti = auth
    await check_permission(db, user, element_name=ELEMENT_NAME, action="create")
    product_db = await create_product(user, data, db)
    return ProductOut.model_validate(product_db)

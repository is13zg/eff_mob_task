from fastapi import APIRouter, Depends
from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.services.user import auth_user
from models.user import User
from schemas.product import ProductIn, ProductOut, ProductUpdate
from core.permisions import check_permission, has_read_all
from core.services.product import create_product, get_all_products, get_own_products, update_product, \
    delete_product, get_product_or_404
from typing import Tuple, List
from models.product import Product

product_router = APIRouter(prefix="/products", tags=["Work with products", ])

ELEMENT_NAME = "products"


@product_router.post("/")
async def create(
        data: ProductIn, auth: Tuple[User, str] = Depends(auth_user), db: AsyncSession = Depends(get_session),
) -> ProductOut:
    user, jti = auth
    await check_permission(db, user, element_name=ELEMENT_NAME, action="create")
    return await create_product(user, data, db)


@product_router.get("/")
async def read_all(
        auth: Tuple[User, str] = Depends(auth_user), db: AsyncSession = Depends(get_session),
) -> List[ProductOut]:
    user, jti = auth
    if await has_read_all(db, user, element_name=ELEMENT_NAME):
        return await get_all_products(db)
    else:
        return await get_own_products(db, user.id)


@product_router.get("/{product_id}")
async def read(product: Product = Depends(get_product_or_404),
               auth: Tuple[User, str] = Depends(auth_user), db: AsyncSession = Depends(get_session),
               ) -> ProductOut:
    user, jti = auth
    await check_permission(db, user, element_name=ELEMENT_NAME, action="read", object_owner_id=product.owner_id)

    return ProductOut.from_orm(product)


@product_router.post("/{product_id}")
async def update(data: ProductUpdate,
                 product: Product = Depends(get_product_or_404),
                 auth: Tuple[User, str] = Depends(auth_user), db: AsyncSession = Depends(get_session),
                 ) -> ProductOut:
    user, jti = auth
    await check_permission(db, user, element_name=ELEMENT_NAME, action="update", object_owner_id=product.owner_id)
    upd_prod = await update_product(data.model_dump(exclude_unset=True), product.id, db)

    return ProductOut.from_orm(upd_prod)


@product_router.delete("/{product_id}")
async def delete(product: Product = Depends(get_product_or_404), auth: Tuple[User, str] = Depends(auth_user),
                 db: AsyncSession = Depends(get_session)) -> dict:
    user, jti = auth
    await check_permission(db, user, element_name=ELEMENT_NAME, action="delete", object_owner_id=product.owner_id)
    await delete_product(product.id, db)

    return {"message": f"product {product.id=} delete", "status": "ok"}

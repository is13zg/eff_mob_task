from fastapi import APIRouter, Depends
from schemas.user import UserRegister, UserOut, UserLogin, TokenOut, UserUpdate
from schemas.product import Product
from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from core.services import register, login, auth_user, logout, delete, update
from core.errors import InvalidCredentials, UserBlocked
from models.user import User
from typing import Tuple

product_router = APIRouter(prefix="/products", tags=["Work with products", ])

@product_router.get("/")
async def get_products(user: User = Depends(auth_user), db: AsyncSession = Depends(get_session)) ->Product:




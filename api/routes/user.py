from fastapi import APIRouter, Depends
from schemas.user import UserRegister, UserOut, UserLogin, TokenOut
from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from core.services import register, login
from core.errors import InvalidCredentials, UserBlocked

user_router = APIRouter(prefix="/user", tags=["Work with user", ])


@user_router.post("/register")
async def register_user(get_user: UserRegister, db: AsyncSession = Depends(get_session)) -> UserOut:
    try:
        db_user = await register(db, **get_user.model_dump(exclude={'rep_passwd'}))

    except IntegrityError as e:
        await db.rollback()
        is_unique_violation = (
                isinstance(getattr(e, "orig", None), UniqueViolationError)
                or getattr(getattr(e, "orig", None), "sqlstate", None) == "23505"
        )
        if is_unique_violation:
            raise HTTPException(status_code=409, detail="Email already registered.")

        raise HTTPException(status_code=500, detail="Database error.")

    return UserOut(id=db_user.id, name=db_user.name)


@user_router.post("/login")
async def login_user(user_login: UserLogin, db: AsyncSession = Depends(get_session)) -> TokenOut:
    try:
        token = await login(db, user_login.email, user_login.passwd)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="No correct user or password")
    except UserBlocked:
        raise HTTPException(status_code=403, detail="User blocker")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Login error")

    return TokenOut(access_token=token)

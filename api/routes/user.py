from fastapi import APIRouter, Depends
from schemas.user import UserRegister, UserOut
from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User

user_router = APIRouter(prefix="/user", tags=["Работа с пользователем", ])


@user_router.post("/register")
async def register_user(user: UserRegister, db: AsyncSession = Depends(get_session)) -> UserOut:
    nu = User(name=user.name,
              last_name=user.last_name,
              father_name=user.father_name,
              email=user.email,
              passwd=user.passwd)
    db.add(nu)
    await db.commit()
    return UserOut(id=1, name="lol")

    # проверить нет ли пользователя с таким емайлом
    # проверить совпадение пароля
    # добавить в базу получить Id

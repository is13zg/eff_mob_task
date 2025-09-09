from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_pass, check_pass, gen_token
from core.repositiry import create_user, get_user_by_email
from core.errors import InvalidCredentials, UserBlocked
from sqlalchemy.exc import NoResultFound
from models.user import User


async def register(db: AsyncSession, name: str, last_name: str, father_name: str, email: str,
                   passwd: str) -> User:
    hash_passwd = hash_pass(passwd)

    async with db.begin():
        user = await create_user(db, name, last_name, father_name, email, hash_passwd)
    return user


async def login(db: AsyncSession, email: str,
                passwd: str) -> str:
    try:
        user = await get_user_by_email(db, email)
    except NoResultFound:
        raise InvalidCredentials

    if not check_pass(passwd, user.passwd):
        raise InvalidCredentials

    if not user.is_active:
        raise UserBlocked

    return gen_token(user.id)

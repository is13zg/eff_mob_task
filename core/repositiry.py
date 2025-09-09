from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from sqlalchemy import select


async def create_user(db: AsyncSession, name: str, last_name: str, father_name: str, email: str,
                      hashed_passwd: str) -> User:
    user = User(name=name, father_name=father_name, last_name=last_name, email=email, passwd=hashed_passwd)
    db.add(user)
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    res = await db.execute(select(User).where(User.email == email))
    user = res.scalar_one()
    return user

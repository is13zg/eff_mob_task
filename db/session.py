from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import settings
from sqlalchemy import text, delete

engine = create_async_engine(
    url=settings.ASYNC_DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_session() -> AsyncSession:
    session = async_session()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def clear_table_data():
    session = get_session()
    try:
        # Очистка таблицы
        await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()

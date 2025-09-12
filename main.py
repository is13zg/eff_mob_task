from fastapi import FastAPI
import uvicorn
from api.routes.user import user_router
from db.session import get_session, engine, async_session

from sqlalchemy import inspect, text
from core.rbac_seed import seed_rbac_minimal
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        tables = await conn.run_sync(lambda c: inspect(c).get_table_names(schema="public"))
        print("Таблицы:", tables)
        try:
            res = await  conn.execute(text("SELECT * FROM role_element_access"))
            print("role_element_access:", res.fetchall())
            ver = await conn.execute(text("SELECT version_num FROM alembic_version"))
            print("alembic_version:", ver.scalar_one())
        except Exception:
            print("Таблицы alembic_version нет (миграции ещё не применялись).")

        # посев RBAC (идемпотентный)
    async with async_session() as session:
        await seed_rbac_minimal(session)

        # отдать управление приложению
    yield

    # --- SHUTDOWN ---
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

from fastapi import FastAPI
import uvicorn
from api.routes.user import user_router
from db.session import get_session, engine
import asyncio
from sqlalchemy import inspect, text

app = FastAPI()
app.include_router(user_router)


async def lol():

    async with engine.begin() as conn:
        # получить список таблиц
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names(schema="public")
        )
        print("Таблицы:", tables)

        # проверить текущую версию Alembic (если таблица есть)
        try:
            ver = await conn.execute(text("SELECT version_num FROM alembic_version"))
            print("alembic_version:", ver.scalar_one())
        except Exception:
            print("Таблицы alembic_version нет (миграции ещё не применялись).")

    await engine.dispose()



if __name__ == "__main__":
    asyncio.run(lol())


    uvicorn.run("main:app", reload=True)

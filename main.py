from fastapi import FastAPI
import uvicorn
from api.routes.user import user_router
from api.routes.product import product_router
from db.session import get_session, engine, async_session

from sqlalchemy import inspect, text
from core.rbac_seed import seed_rbac_minimal
from contextlib import asynccontextmanager
from pprint import pprint


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with async_session() as session:
        await seed_rbac_minimal(session)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(product_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

from fastapi import FastAPI
import uvicorn
from api.routes.user import user_router
from db.base import init_models

app = FastAPI()
app.include_router(user_router)

if __name__ == "__main__":
    init_models()
    uvicorn.run("main:app", reload=True)

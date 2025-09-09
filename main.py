from fastapi import FastAPI
import uvicorn
from api.routes.user import user_router

from db.session import clear_table_data

app = FastAPI()
app.include_router(user_router)

if __name__ == "__main__":

    #clear_table_data()
    uvicorn.run("main:app", reload=True)

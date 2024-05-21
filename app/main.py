from fastapi import FastAPI

from app.routers import auth_api, category_api, user_api

app = FastAPI()


app.include_router(auth_api.router)
app.include_router(user_api.router)
app.include_router(category_api.router)

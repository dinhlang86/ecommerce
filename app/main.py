from fastapi import FastAPI, status

from app.routers import auth_api, user_api

app = FastAPI()


@app.get("/healthy", status_code=status.HTTP_200_OK)
def check_healthy() -> dict[str, str]:
    return {"message": "I am healthy!"}


app.include_router(auth_api.router)
app.include_router(user_api.router)

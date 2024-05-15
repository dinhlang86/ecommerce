from fastapi import FastAPI, status


app = FastAPI()


@app.get("/healthy", status_code=status.HTTP_200_OK)
def check_healthy() -> dict[str, str]:
    return {"message": "I am healthy!"}

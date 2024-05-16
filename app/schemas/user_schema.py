from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    name: str
    password: str
    role: str

from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    email: str
    name: str
    password: str = Field(min_length=6)
    role: str


class PutUserPassword(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

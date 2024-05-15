from sqlmodel import SQLModel, Field, Enum, Column
from typing import Optional
import enum


class Role(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    email: str
    password: str
    role: Role = Field(sa_column=Column(Enum(Role), default=Role.user, nullable=False))

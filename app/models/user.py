import enum
from dataclasses import dataclass
from typing import Optional

from sqlmodel import Column, Enum, Field, SQLModel


class Role(str, enum.Enum):
    admin = "admin"
    user = "user"


class DisplayUser(SQLModel):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    email: str
    role: Role = Field(sa_column=Column(Enum(Role), default=Role.user, nullable=False))


# Create User model with email as username and password to login to the application
class User(DisplayUser, table=True):
    password: str


@dataclass
class TokenUser:
    """User model that is extracted from the token."""

    username: str
    id: int
    role: Role

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import relationship
from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text

# resolve circular import
if TYPE_CHECKING:
    from app.models.cart_item import CartItem

from app.models.user import User


class CartBase(SQLModel):
    created_date: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )


class Cart(CartBase, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="carts")
    cart_items: list["CartItem"] = Relationship(
        sa_relationship=relationship("CartItem", cascade="all, delete", back_populates="cart")
    )

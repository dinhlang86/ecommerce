from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import relationship
from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text

from app.models.user import User

# resolve circular import
if TYPE_CHECKING:
    from app.models.cart_item import CartItem


class CartBase(SQLModel):
    created_date: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    user_id: int = Field(foreign_key="user.id")


class Cart(CartBase, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    user: User = Relationship(back_populates="carts")
    cart_items: list["CartItem"] = Relationship(
        sa_relationship=relationship(
            "CartItem", cascade="all, delete", back_populates="cart", lazy="selectin"
        )
    )

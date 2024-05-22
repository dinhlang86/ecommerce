from datetime import datetime
from typing import Optional

from sqlalchemy.orm import relationship
from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text

from app.models.product import Product
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
        sa_relationship=relationship(
            "CartItem", cascade="all, delete", back_populates="cart", lazy="selectin"
        )
    )


class CartCreate(CartBase):
    pass


class CartPublic(CartBase):
    id: int
    user_id: int


class CartItemBase(SQLModel):
    created_date: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    product_id: int = Field(foreign_key="product.id")


class CartItem(CartItemBase, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    product: Product = Relationship()
    cart_id: int = Field(foreign_key="cart.id")
    cart: Cart = Relationship(back_populates="cart_items")


class CartItemCreate(CartItemBase):
    pass


class CartItemPublic(CartItemBase):
    id: int


class CartPublicWithItems(CartPublic):
    cart_items: list[CartItemPublic] = []

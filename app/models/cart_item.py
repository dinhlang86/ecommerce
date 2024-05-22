from datetime import datetime
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text

from app.models.cart import Cart
from app.models.product import Product


class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    created_date: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship()
    cart_id: int = Field(foreign_key="cart.id")
    cart: Cart = Relationship(back_populates="cart_items")

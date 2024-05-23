import enum
from datetime import date
from typing import Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from app.models.user import User


class Status(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    shipping = "shipping"
    delivered = "delivered"


class OrderBase(SQLModel):
    order_date: Optional[date] = Field(default_factory=date.today, nullable=False)
    order_amount: int
    order_status: Status = Field(
        sa_column=Column(Enum(Status), default=Status.pending, nullable=False)
    )
    shipping_address: str


class Order(OrderBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="orders")
    order_items: Optional[list["OrderItem"]] = Relationship(back_populates="order")


class OrderCreate(OrderBase):
    pass


class OrderPublic(OrderBase):
    id: int
    user_id: int


class OrderItemBase(SQLModel):
    quantity: int
    created_date: Optional[date] = Field(default_factory=date.today, nullable=False)


class OrderItem(OrderItemBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    order: Order = Relationship(back_populates="order_items")


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemPublic(OrderItemBase):
    id: int


class OrderPublicWithItems(OrderPublic):
    order_items: list[OrderItemPublic] = []

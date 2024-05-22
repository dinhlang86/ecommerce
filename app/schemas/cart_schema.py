from app.models.cart import CartBase
from app.models.cart_item import CartItemBase


class CartCreate(CartBase):
    pass


class CartPublic(CartBase):
    id: int


class CartPublicWithItems(CartPublic):
    cart_items: "list[CartItemPublic]" = []


class CartItemCreate(CartItemBase):
    pass


class CartItemPublic(CartItemBase):
    id: int

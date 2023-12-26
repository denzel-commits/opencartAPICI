from pydantic import BaseModel


class TotalsItem(BaseModel):
    title: str
    text: str


class Product(BaseModel):
    cart_id: str
    product_id: str
    name: str
    model: str
    option: list
    quantity: int
    stock: bool
    shipping: int
    price: str
    total: str
    reward: int


class Cart(BaseModel):
    products: list[Product]
    vouchers: list
    totals: list[TotalsItem]

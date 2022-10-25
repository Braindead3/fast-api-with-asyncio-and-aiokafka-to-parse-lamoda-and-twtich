from typing import Optional

from pydantic import BaseModel


class UpdateProduct(BaseModel):
    id: Optional[int] = None
    href: Optional[str] = None
    name: Optional[str] = None
    price: Optional[str] = None
    brand: Optional[str] = None


class Product(BaseModel):
    id: int
    href: str
    name: str
    price: str
    brand: str

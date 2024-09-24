from typing import TypedDict

from pydantic import BaseModel

class ProductTypedDict(TypedDict):
    id: int
    name: str
    price: int
    image_name: str | None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    image_name: str | None

    @classmethod
    def build(cls, product: ProductTypedDict):
        return cls(
            id=product['id'],
            name=product['name'],
            price=product['price'],
            image_name=product['image_name'],
        )

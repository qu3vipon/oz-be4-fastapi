from pydantic import BaseModel

class UpdateProductRequest(BaseModel):
    name: str | None = None
    price: int | None = None

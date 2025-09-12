from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=30, default="some_product")
    count: int = Field(..., default=0, ge=0)
    price: float = Field(..., default=0, ge=0)

from pydantic import BaseModel, Field


class ProductIn(BaseModel):
    name: str = Field(..., min_length=3, max_length=30)
    count: int = Field(..., ge=0)
    price: float = Field(..., ge=0)


class ProductOut(ProductIn):
    id: int

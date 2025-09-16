from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ProductIn(BaseModel):
    name: str = Field(..., min_length=3, max_length=30)
    count: int = Field(..., ge=0)
    price: float = Field(..., ge=0)


class ProductOut(ProductIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(ProductIn):
    name: Optional[str] = Field(None, min_length=3, max_length=30)
    count: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)

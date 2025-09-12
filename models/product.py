from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import List
from db.base import Base, PkMixin, TimestampMixin


class Product(Base, PkMixin, TimestampMixin):
    __tablename__ = "products"
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    count: Mapped[int] = mapped_column(nullable=False, default=0)
    price: Mapped[float] = mapped_column(nullable=False, default=0)

    owner: Mapped["User"] = relationship(
        back_populates="products",
        lazy="joined",

    )

    def __repr__(self) -> str:
        """Строковое представление объекта для удобства отладки."""
        return f"<{self.__class__.__name__}({self.id=}, {self.name=}, {self.owner_id=})>"

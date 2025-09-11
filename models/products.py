from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import List
from db.base import Base, PkMixin, TimestampMixin


class Product(Base, PkMixin, TimestampMixin):
    name: Mapped[str] = mapped_column(String(30))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)


    owner : Mapped['User'] = relationship(
        back_populates="products",
        lazy="joined",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Строковое представление объекта для удобства отладки."""
        return f"<{self.__class__.__name__}({self.id=}, {self.name=}, {self.name=})>"

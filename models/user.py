from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean
from typing import List
from db.base import Base, PkMixin, TimestampMixin


class User(Base, PkMixin, TimestampMixin):
    name: Mapped[str]
    last_name: Mapped[str]
    father_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    passwd: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    roles: Mapped[List['Role']] = relationship(
        secondary="user_roles",
        back_populates="users",
        lazy="selectin"
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="owner",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        """Строковое представление объекта для удобства отладки."""
        return f"<{self.__class__.__name__}({self.id=}, {self.email=}, {self.is_active=})>"

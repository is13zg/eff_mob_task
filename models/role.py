from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship,
from typing import List
from sqlalchemy import ForeignKey, String


class role(Base):
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    users: Mapped[List['User']] = relationship(
        secondary="user_roles",
        back_populates="users",
        lazy="selectin"
    )
    acces_rule: Mapped[List['RoleElementAcces']] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class UserRole(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)

from db.base import Base, PkMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import ForeignKey, String
import enum


class ActionEnum(str, enum.Enum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"


class LevelEnun(str, enum.Enum):
    none = "none"
    own = "own"
    all = "all"


class Role(Base, PkMixin):
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    users: Mapped[List['User']] = relationship(
        secondary="user_roles",
        back_populates="roles",
        lazy="selectin"
    )
    acces_rule: Mapped[List['RoleElementAcces']] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)


class RoleElementAcces(Base):
    __tablename__ = "role_element_access"
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    element_id: Mapped[int] = mapped_column(ForeignKey("elements.id", ondelete="CASCADE"), primary_key=True)
    action: Mapped[ActionEnum] = mapped_column(default=ActionEnum.read, primary_key=True)
    level: Mapped[LevelEnun] = mapped_column(default=LevelEnun.none, nullable=False)

    role: Mapped['Role'] = relationship(
        back_populates='acces_rule',
        lazy="joined"
    )
    element: Mapped['ResourceElement'] = relationship(
        back_populates='acces_rule',
        lazy="joined"
    )

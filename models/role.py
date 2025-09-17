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


class LevelEnum(str, enum.Enum):
    none = "none"
    own = "own"
    all = "all"


class Role(Base, PkMixin):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    users: Mapped[List["User"]] = relationship(
        secondary="user_roles",
        back_populates="roles",
        lazy="selectin",
    )
    access_rule: Mapped[List["RoleElementAccess"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)


class RoleElementAccess(Base):
    __tablename__ = "role_element_access"
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    element_id: Mapped[int] = mapped_column(ForeignKey("resourse_elements.id", ondelete="CASCADE"), primary_key=True)
    action: Mapped[ActionEnum] = mapped_column(default=ActionEnum.read, primary_key=True)
    level: Mapped[LevelEnum] = mapped_column(default=LevelEnum.none, nullable=False)

    role: Mapped["Role"] = relationship(back_populates="access_rule", lazy="joined")
    element: Mapped["ResourseElement"] = relationship(back_populates="access_rule", lazy="joined")







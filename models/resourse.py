from db.base import Base, PkMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List


class ResourseElement(Base, PkMixin):
    __tablename__ = "resourse_elements"
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    access_rule: Mapped[List["RoleElementAccess"]] = relationship(
        back_populates="element",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

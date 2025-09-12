from db.base import Base, PkMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List

class RecourseElement(Base, PkMixin):
    __tablename__ = "recourse_elements"
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    # одно имя на обеих сторонах связи!
    access_rule: Mapped[List["RoleElementAccess"]] = relationship(
        back_populates="element",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

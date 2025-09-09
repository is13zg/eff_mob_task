from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean

from db.base import Base


class User(Base):
    name: Mapped[str]
    last_name: Mapped[str]
    father_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    passwd: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")


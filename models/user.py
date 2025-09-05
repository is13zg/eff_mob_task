from sqlalchemy.orm import Mapped

from db.base import Base


class User(Base):
    name: Mapped[str]
    last_name: Mapped[str]
    father_name: Mapped[str]
    email: Mapped[str]
    passwd: Mapped[str]

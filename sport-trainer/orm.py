from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime
from bcrypt import gensalt, hashpw

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shortname: Mapped[str] = mapped_column(String(80), nullable=False)
    fullname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column(String(60))
    created: Mapped[datetime] = mapped_column(default=datetime.now())

    def __init__(self, email:str, shortname:str, fullname:str = None, password:str = None):
        super().__init__()
        self.shortname = shortname
        self.fullname = fullname
        self.email = email
        self.set_password(password)

    def set_password(self, password:str):
        assert(password is not None)
        self.password = hashpw(password.encode('utf-8'), gensalt())

    def __str__(self):
        return (super().__str__()[:-1] +
                f" - {self.id} {self.shortname} - {self.fullname} - {self.email} - {self.password} - {self.created}>")
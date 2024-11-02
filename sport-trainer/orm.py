from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime, timedelta, UTC
from bcrypt import gensalt, hashpw, checkpw

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shortname: Mapped[str] = mapped_column(String(80), nullable=False)
    fullname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column(String(60))
    created: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    session: Mapped[datetime] = mapped_column(nullable=True)

    def __init__(self, email:str, shortname:str, fullname:str = None, password:str = None, session:datetime = None):
        super().__init__()
        self.shortname = shortname
        self.fullname = fullname
        self.email = email
        self.set_password(password)
        self.session: datetime = session

    def set_password(self, password:str):
        assert(password is not None)
        self.password = hashpw(password.encode('utf-8'), gensalt())

    def test_password(self, password:str):
        assert(password is not None)
        return checkpw(password.encode('utf-8'), self.password)

    def set_session(self, duration=4):
        self.session = datetime.now(UTC) + timedelta(hours=duration)

    def session_valid(self) -> bool:
        if self.session is None:
            return False
        else:
            s = self.session.replace(tzinfo=UTC)
            return s > datetime.now(UTC)

    def __repr__(self):
        return f"<User - #{self.id} - {self.shortname} - {self.fullname} - {self.email} - {self.password} - \
{self.created} - {self.session if self.session_valid() else "expired"} >"
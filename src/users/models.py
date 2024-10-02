import re
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Index

from core.database.orm import Base


class User(Base):
    __tablename__ = "service_user"
    id = Column(Integer, primary_key=True)
    username = Column(String(16))
    password = Column(String(60))
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint("username", name="uix_service_user_username"),
        Index("ix_service_user_created_at", "created_at"),
    )


    @staticmethod
    def _validate_hash(password_hash: str) -> None:
        bcrypt_pattern = r'^\$2[aby]\$[0-9]{2}\$[./A-Za-z0-9]{53}$'
        assert re.match(bcrypt_pattern, password_hash) is not None

    @classmethod
    def create(cls, username: str, password: str):
        cls._validate_hash(password_hash=password)
        return cls(username=username, password=password)

    def update_password(self, new_password: str):
        self._validate_hash(password_hash=new_password)
        self.password = new_password

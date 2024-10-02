from sqlalchemy import exists
from sqlalchemy.orm import Session
from fastapi import Depends
from core.database.connection import get_db
from users.models import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def save(self, user: User):
        self.db.add(user)
        self.db.commit()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def validate_username(self, username: str) -> bool:
        # Exists=True -> validate=False / Exists=False -> validate=True
        return not self.db.query(exists().where(User.username == username)).scalar()

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

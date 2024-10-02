from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel

from users.models import User


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None
    created_at: datetime

    @classmethod
    def build(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )


class UserTokenResponse(BaseModel):
    access_token: str

    @classmethod
    def build(cls, access_token: str):
        return cls(access_token=access_token)

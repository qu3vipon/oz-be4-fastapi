from typing import TypedDict

from pydantic import BaseModel


class UserTypedDict(TypedDict):
    id: int
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    password: str

    @classmethod
    def build(cls, user: UserTypedDict):
        return cls(id=user['id'], username=user['username'], password=user['password'])


class UserTokenResponse(BaseModel):
    access_token: str

    @classmethod
    def build(cls, access_token: str):
        return cls(access_token=access_token)

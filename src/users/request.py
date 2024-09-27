from pydantic import BaseModel


class UserAuthRequest(BaseModel):
	username: str
	password: str


class UpdateUserRequest(BaseModel):
	password: str

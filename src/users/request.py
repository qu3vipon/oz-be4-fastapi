from pydantic import BaseModel, constr, Field


EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

class UserAuthRequest(BaseModel):
	username: str
	password: str


class UpdateUserRequest(BaseModel):
	password: str


class UserOTPRequest(BaseModel):
	email: constr(pattern=EMAIL_PATTERN) = Field(examples=["example@email.com"])


class UserOTPVerifyRequest(BaseModel):
	email: constr(pattern=EMAIL_PATTERN) = Field(examples=["example@email.com"])
	otp: int = Field(..., ge=100_000, le=999_999)

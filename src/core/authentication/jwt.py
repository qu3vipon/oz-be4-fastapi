from fastapi import status, HTTPException

import time
from typing import TypedDict

import jwt

from core.config import settings

class JWTPayloadTypedDict(TypedDict):
    username: str
    isa: float  # issued at (UNIX timestamp)


class JWTService:
    JWT_SECURITY_KEY = settings.jwt_security_key
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRY_SECONDS = 24 * 60 * 60  # 하루: 24시간 * 60분 * 60초

    def create_access_token(self, username: str) -> str:
        payload: JWTPayloadTypedDict = {"username": username, "isa": time.time()}
        return jwt.encode(payload=payload, key=self.JWT_SECURITY_KEY, algorithm=self.JWT_ALGORITHM)

    def decode_access_token(self, access_token: str) -> JWTPayloadTypedDict:
        try:
            return jwt.decode(jwt=access_token, key=self.JWT_SECURITY_KEY, algorithms=[self.JWT_ALGORITHM])
        except jwt.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid JWT",
            )

    def is_valid_token(self, payload: JWTPayloadTypedDict) -> bool:
        return time.time() < payload["isa"] + self.JWT_EXPIRY_SECONDS

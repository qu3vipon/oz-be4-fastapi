from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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

    def _decode_access_token(self, access_token: str) -> JWTPayloadTypedDict:
        try:
            return jwt.decode(jwt=access_token, key=self.JWT_SECURITY_KEY, algorithms=[self.JWT_ALGORITHM])
        except jwt.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid JWT",
            )

    def _is_valid_token(self, payload: JWTPayloadTypedDict) -> bool:
        return time.time() < payload["isa"] + self.JWT_EXPIRY_SECONDS

    def _get_jwt(
        self, auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
    ) -> str:
        if auth_header is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="JWT Not provided",
            )
        return auth_header.credentials

    def get_username(self, access_token: str = Depends(_get_jwt)):
        payload: JWTPayloadTypedDict = self._decode_access_token(access_token=access_token)
        if not self._is_valid_token(payload=payload):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Expired",
            )
        return payload["username"]

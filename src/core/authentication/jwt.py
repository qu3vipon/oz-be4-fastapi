from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import time
from typing import TypedDict

import jwt

JWT_SECURITY_KEY = "0f22c7c8644ba6995cb8f5798ab85c1daa049f274c8c84206be014507acd6f4a"
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_SECONDS = 24 * 60 * 60  # 하루: 24시간 * 60분 * 60초


class JWTPayloadTypedDict(TypedDict):
    username: str
    isa: float  # issued at (UNIX timestamp)


def create_access_token(username: str) -> str:
    payload: JWTPayloadTypedDict = {"username": username, "isa": time.time()}
    return jwt.encode(payload=payload, key=JWT_SECURITY_KEY, algorithm=JWT_ALGORITHM)


def _decode_access_token(access_token: str) -> JWTPayloadTypedDict:
    try:
        return jwt.decode(jwt=access_token, key=JWT_SECURITY_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT",
        )


def _is_valid_token(payload: JWTPayloadTypedDict) -> bool:
    return time.time() < payload["isa"] + JWT_EXPIRY_SECONDS


def _get_jwt(
    auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
) -> str:
    if auth_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT Not provided",
        )
    return auth_header.credentials


def get_username(access_token: str = Depends(_get_jwt)):
    payload: JWTPayloadTypedDict = _decode_access_token(access_token=access_token)
    if not _is_valid_token(payload=payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Expired",
        )
    return payload["username"]

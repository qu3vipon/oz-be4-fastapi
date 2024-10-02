from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from core.authentication.jwt import JWTPayloadTypedDict, JWTService


def _get_jwt(
    auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
) -> str:
    if auth_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT Not provided",
        )
    return auth_header.credentials

def get_username(
    access_token: str = Depends(_get_jwt),
    jwt_service: JWTService = Depends(),
):
    payload: JWTPayloadTypedDict = jwt_service.decode_access_token(access_token=access_token)
    if not jwt_service.is_valid_token(payload=payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Expired",
        )
    return payload["username"]

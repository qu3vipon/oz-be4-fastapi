import time

import jwt

JWT_SECURITY_KEY = "0f22c7c8644ba6995cb8f5798ab85c1daa049f274c8c84206be014507acd6f4a"
JWT_ALGORITHM = "HS256"


def create_access_token(username: str) -> str:
    payload = {"username": username, "isa": time.time()}
    return jwt.encode(payload=payload, key=JWT_SECURITY_KEY, algorithm=JWT_ALGORITHM)

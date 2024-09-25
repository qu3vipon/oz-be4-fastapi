import bcrypt


def hash_password(plain_text: str) -> str:
    hashed_password_bytes: bytes = bcrypt.hashpw(
		plain_text.encode("utf-8"), bcrypt.gensalt()
	)
    return hashed_password_bytes.decode("utf-8")


def check_password(plain_text: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
		plain_text.encode("utf-8"),
		hashed_password.encode("utf-8"),
	)

import random

from redis import Redis

redis_client = Redis(
    host="127.0.0.1", port=63790, db=0, encoding="utf-8", decode_responses=True
)

class OTPService:
    def __init__(self):
        self.redis_client = redis_client

    def otp_exists(self, email: str) -> bool:
        return bool(self.redis_client.get(email))

    @staticmethod
    def _create_otp():
        return random.randint(100_000, 999_999)

    def create_otp(self, email: str) -> int:
        otp: int = self._create_otp()
        self.redis_client.setex(name=email, time=3 * 60, value=otp)
        return otp

    def validate_otp(self, email: str, otp: int) -> bool:
        cached_otp: str | None = self.redis_client.get(email)
        if not cached_otp:
            return False
        return str(otp) == cached_otp

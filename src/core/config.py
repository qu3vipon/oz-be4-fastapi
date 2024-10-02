import os
from enum import StrEnum
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerEnv(StrEnum):
     LOCAL = "local"  # 내 개발환경(PC)
     DEV = "dev"      # 프론트개발자, QA 사용하는 환경
     PROD = "prod"    # 사용자들이 사용하는 실제 환경


# linux 환경 변수
SERVER_ENV = os.getenv("ENV", ServerEnv.LOCAL)


# 1. 명시적으로 Settings Class를 분리하는 방법
# class LocalSettings(BaseSettings):
#     database_url: str
#     jwt_security_key: str
#
#     model_config = SettingsConfigDict(env_file="core/.env.local")
#
# class DevSettings(BaseSettings):
#     database_url: str
#     jwt_security_key: str
#
#     model_config = SettingsConfigDict(env_file="core/.env.dev")
#
#
# class ProdSettings(BaseSettings):
#     database_url: str
#     jwt_security_key: str
#
#     model_config = SettingsConfigDict(env_file="core/.env.prod")
#
#
# def get_settings(env: ServerEnv) -> BaseSettings:
#     match env:
#         case ServerEnv.DEV:
#             return DevSettings()
#         case ServerEnv.PROD:
#             return ProdSettings()
#         case _:
#             return LocalSettings()


# 2. Settings 공유하고, 환경변수에 따라서 다른 값 주입
class Settings(BaseSettings):
    database_url: str
    jwt_security_key: str

    model_config = SettingsConfigDict(env_file=f"core/.env.{SERVER_ENV}")


settings = Settings()

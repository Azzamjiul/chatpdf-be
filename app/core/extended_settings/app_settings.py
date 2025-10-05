from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    APP_NAME: str = "FastAPI Template"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "FastAPI Template API"

    DEBUG: bool = False

    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]

    JWT_SECRET: str = "your-secret-key"
    JWT_TOKEN_EXPIRE: int = 60
    # Refresh token expiry in minutes (default 7 days)
    JWT_REFRESH_TOKEN_EXPIRE: int = 60 * 24 * 7
    # Algorithm used to sign JWTs
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

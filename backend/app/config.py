from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "韩语启蒙助手 API"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+asyncpg://korean_app:korean_app_dev@postgres:5432/korean_app"
    DATABASE_URL_SYNC: str = "postgresql://korean_app:korean_app_dev@postgres:5432/korean_app"
    REDIS_URL: str = "redis://redis:6379/0"
    SECRET_KEY: str = "dev-secret-change-in-production-!!"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    S3_ENDPOINT: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "korean-audio"

    model_config = {"env_file": ".env"}


settings = Settings()

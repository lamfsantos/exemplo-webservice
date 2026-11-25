from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    JWT_SECRET: str = "super_secret_jwt_token_desafio_mobile_2026_ifms"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    PORT: int = 10000

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://novin:novin@postgres:5432/novin_social"
    redis_url: str = "redis://redis:6379/0"
    openai_api_key: str | None = None

    x_bearer_token: str | None = None
    x_search_url: str = "https://api.x.com/2/tweets/search/recent"
    connector_timeout_seconds: float = 20.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = "7677506032:AAHB2QtrxKdgUXLWlE2xXaVxs9V7BPz1fhc"
    TELEGRAM_CHAT_ID: str = "5057752127"

    class Config:
        env_file = ".env"


settings = Settings()

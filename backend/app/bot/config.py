from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = "7677506032:AAHduD5EePz3bE23DKlo35KoOp2_9lZuS34"
    TELEGRAM_CHAT_ID: str = "5057752127"

    class Config:
        env_file = ".env"


settings = Settings()

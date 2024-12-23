from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = "7677506032:AAHoVqFJs3IZKNK2NVzGnzKUn1hjVtU5Ryk"
    TELEGRAM_CHAT_ID: str = "5057752127"

    class Config:
        env_file = ".env"


settings = Settings()

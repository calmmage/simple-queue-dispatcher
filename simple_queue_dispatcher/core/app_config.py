from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    conn_str: str
    name: str

    class Config:
        env_prefix = 'DATABASE_'


class TelegramBotConfig(BaseSettings):
    token: str

    class Config:
        env_prefix = 'TELEGRAM_BOT_'


class AppConfig(BaseSettings):
    database: DatabaseConfig
    telegram_bot: TelegramBotConfig

    def __init__(self, *args, **kwargs):
        database = DatabaseConfig(*args, **kwargs)
        telegram_bot = TelegramBotConfig(*args, **kwargs)
        super().__init__(*args, **kwargs, database=database,
                         telegram_bot=telegram_bot)

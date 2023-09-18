from bot_base.core import AppConfig, DatabaseConfig, TelegramBotConfig


class SQDDatabaseConfig(DatabaseConfig):
    pass


class SQDTelegramBotConfig(TelegramBotConfig):
    pass


class SQDAppConfig(AppConfig):
    _database_config_class = SQDDatabaseConfig
    _telegram_bot_config_class = SQDTelegramBotConfig

from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    conn_str: str
    name: str

    class Config:
        env_prefix = 'DATABASE_'


class AppConfig(BaseSettings):
    database: DatabaseConfig

    def __init__(self, *args, **kwargs):
        database = DatabaseConfig(*args, **kwargs)
        super().__init__(*args, **kwargs, database=database)

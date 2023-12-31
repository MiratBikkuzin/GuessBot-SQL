from environs import Env
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str


@dataclass
class TgBot:
    bot_token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    
    env: Env = Env()
    env.read_env(path=path)

    return Config(
        tg_bot=TgBot(
            bot_token=env('BOT_TOKEN')
        ),
        db=DatabaseConfig(
            host=env('DB_HOST'),
            port=env.int('DB_PORT'),
            name=env('DATABASE'),
            user=env('DB_USER'),
            password=env('DB_PASSWORD')
        )
    )
from details.db_queries import *
from details.emojize import *
from environs import Env


env: Env = Env()
env.read_env()


bot_token: str = env('BOT_TOKEN')
db_host: str = env('DB_HOST')
db_port: int = env.int('DB_PORT')
database: str = env('DATABASE')
db_user: str = env('DB_USER')
db_password: str = env('DB_PASSWORD')
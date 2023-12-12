from asyncio import ProactorEventLoop
from config_data.config import Config
from aiomysql.utils import _PoolAcquireContextManager
import aiomysql


async def db_connection(running_loop: ProactorEventLoop, config: Config) -> tuple[aiomysql.Pool, _PoolAcquireContextManager]:
    global connection
    
    pool: aiomysql.Pool = await aiomysql.create_pool(
        loop=running_loop,
        user=config.db.user,
        password=config.db.password,
        db=config.db.name,
        host=config.db.host,
        port=config.db.port,
        autocommit=True
    )

    async with pool.acquire() as connection:
        pass

    return pool, connection


async def execute_query(query: str, main_command: str) -> tuple | None:
    async with connection.cursor() as cursor:
        await cursor.execute(query)
        if main_command.lower() == 'select':
            return await cursor.fetchone()
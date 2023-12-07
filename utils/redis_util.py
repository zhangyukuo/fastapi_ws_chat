from redis import asyncio as aioredis
# from aioredis import ConnectionsPool
from config.get_config import config

url = (config['db_redis']['host'], config['db_redis']['port'])
host = config['db_redis']['host']
db = config['db_redis']['db']
timeout = config['db_redis']['timeout']
password = config['db_redis']['password']
port = config['db_redis']['port']


# aioredis==2.0.0
async def get_redis():
    # Redis client bound to pool of connections (auto-reconnecting).
    redis = aioredis.from_url(
        "redis://{}".format(host), db=db, password=password, port=port, encoding="utf-8", decode_responses=True
    )
    yield redis

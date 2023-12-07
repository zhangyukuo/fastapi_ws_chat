import uvicorn
from fastapi import FastAPI
import asyncio
import aioredis
import json
import os
from app.chat_manager import chat
from config.get_config import config

# redis配置
url = (config['db_redis']['host'], config['db_redis']['port'])
host = config['db_redis']['host']
db = config['db_redis']['db']
timeout = config['db_redis']['timeout']
password = config['db_redis']['password']
port = config['db_redis']['port']


# 初始化app
app = FastAPI(title="Ws Chat", description="测试", version="1.0.0")
app.openapi_version = "3.0.0"


app.include_router(chat.app, prefix='/api/chat', tags=['Chat'])


@app.on_event('startup')
async def on_startup():
    print(f"订阅初始化:{os.getpid()}")
    # 执行消息订阅机制https://aioredis.readthedocs.io/en/latest/examples/
    loop = asyncio.get_event_loop()
    loop.create_task(register_pubsub())


async def reader(channel):
    # 进行消息的消费
    async for msg in channel.listen():
        # print(msg)
        msg_data = msg.get("data")
        if msg_data and isinstance(msg_data, str):
            msg_data_dict = json.loads(msg_data)
            print(f"chat:{msg_data_dict}")
            sender = msg_data_dict.get("sender")
            # 进行消息处理
            await chat.cm.handle_websocket_message(msg_data_dict, sender)


async def register_pubsub():
    pool = aioredis.from_url(
        "redis://{}".format(host), db=db, password=password, port=port, encoding="utf-8", decode_responses=True
    )
    psub = pool.pubsub()

    async with psub as p:
        # 消息订阅
        await p.subscribe("chat")
        await reader(p)
        await p.unsubscribe("chat")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)


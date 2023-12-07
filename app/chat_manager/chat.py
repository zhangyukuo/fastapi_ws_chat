from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.chat_manager.server import ConnectionManager
from pydantic import BaseModel, Field
from utils.redis_util import get_redis
import json

app = APIRouter()

cm = ConnectionManager()

MAIN_BASE = "http://localhost:8004"  # 主程序


@app.websocket("/connect_chat")
async def connect_chat(websocket: WebSocket, user_code: str):
    try:

        await cm.connect(websocket, user_code)

    except WebSocketDisconnect:
        # 连接断开时移除连接
        del cm.websocket_connections[user_code]


class DiagnosisChatSch(BaseModel):
    msg: str = Field(None, title="信息")
    sender: str = Field(None, title="发送者")
    recipient: str = Field(None, title="接收者")


@app.post("/create_chat", summary="发起聊天")
async def create_chat(param: DiagnosisChatSch, r=Depends(get_redis)):
    """

    """

    ws_param = {"type": "private_message",
                "msg": param.msg,
                "sender": param.sender,
                "recipient": param.recipient}

    await r.publish('diagnosis_chat', json.dumps(ws_param))

    return {'code': 200, 'msg': '成功', 'data': ''}

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        # 保存当前所有的链接的websocket对象
        self.websocket_connections = {}

    async def connect(self, websocket: WebSocket, client_id):
        # 添加连接并发送欢迎消息
        await websocket.accept()
        self.websocket_connections[client_id] = websocket
        await websocket.send_json({"type": "system",
                                   "msg": "Welcome to the chat app!",
                                   "sender": "system",
                                   "recipient": client_id})

        try:
            # 处理消息
            while True:
                # 获取信息
                message = await websocket.receive_json()
                # 处理发送信息
                await self.handle_websocket_message(message, client_id)

        except WebSocketDisconnect:
            # 连接断开时移除连接
            del self.websocket_connections[client_id]

    async def handle_websocket_message(self, message: dict, client_id):

        # 处理私聊消息
        if message.get("type") == "private_message":
            recipient = message.get("recipient")
            msg = message.get("msg")
            recipient_conn = self.websocket_connections.get(recipient)

            if recipient_conn:
                # 在线
                await recipient_conn.send_json({"type": "private_message",
                                                "sender": client_id,
                                                "msg": msg,
                                                "recipient": recipient})

    async def broadcast(self, message: dict):
        # 循环变量给所有在线激活的链接发送消息-全局广播
        for connection in self.websocket_connections:
            await connection.send_text(message)

    async def close(self, websocket: WebSocket, client_id):
        # 断开客户端的链接
        await websocket.close()
        del self.websocket_connections[client_id]

    async def disconnect(self, user_id):
        websocket: WebSocket = self.websocket_connections[user_id]
        await websocket.close()
        del self.websocket_connections[user_id]

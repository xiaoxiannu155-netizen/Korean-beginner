"""WebSocket handler for real-time AI chat"""
import json
from fastapi import WebSocket, WebSocketDisconnect
from app.services.ws_chat_service import generate_chat_response, get_chat_starter


class ChatConnectionManager:
    """Manages active WebSocket chat connections"""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

        # Send welcome message
        starter = get_chat_starter()
        await websocket.send_json({
            "type": "welcome",
            "reply": starter["ko"],
            "reply_zh": starter["zh"],
            "reply_pronunciation": starter.get("pron"),
        })

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def handle_message(self, websocket: WebSocket, user_id: str, message: str):
        """Process incoming chat message and send response"""
        try:
            # Echo the user message
            await websocket.send_json({
                "type": "echo",
                "user_message": message,
            })

            # Generate and send AI response
            response = generate_chat_response(message)
            await websocket.send_json({
                "type": "response",
                **response,
            })
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "message": str(e),
            })


chat_manager = ChatConnectionManager()


async def handle_chat_websocket(websocket: WebSocket, user_id: str):
    """Main WebSocket handler for chat"""
    await chat_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            if user_message:
                await chat_manager.handle_message(websocket, user_id, user_message)
    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)
    except Exception:
        chat_manager.disconnect(user_id)

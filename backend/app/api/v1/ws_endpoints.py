"""WebSocket endpoint definitions for FastAPI router"""
from fastapi import APIRouter, WebSocket, Depends, Query
from app.services.auth_service import decode_token
from app.websocket.chat_ws import handle_chat_websocket

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    token: str = Query(...),
):
    """WebSocket endpoint for AI chat.

    Connect with: ws://host/ws/chat?token=JWT_TOKEN
    """
    # Validate token
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        await websocket.close(code=4001, reason="Invalid token")
        return

    user_id = payload.get("sub")
    if not user_id:
        await websocket.close(code=4001, reason="Invalid user")
        return

    await handle_chat_websocket(websocket, user_id)

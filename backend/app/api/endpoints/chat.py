from fastapi import APIRouter, Depends, HTTPException, WebSocket, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.core.auth import get_current_user
from app.core.ws_auth import get_current_user_ws
from app.models.user import User
from app.schemas.chat import (
    Chat, ChatCreate,
    Message, MessageCreate,
    ChatFile, ChatFileCreate
)

router = APIRouter()

@router.websocket("/ws")
async def chat_websocket(
    websocket: WebSocket,
    db: Session = Depends(get_db)
):
    user = await get_current_user_ws(websocket, db)
    if not user:
        return
    
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Обработка сообщений
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

@router.post("/", response_model=Chat)
def create_chat(
    chat: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new chat."""
    # Здесь будет логика создания чата
    pass

@router.get("/", response_model=List[Chat])
def get_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all chats for current user."""
    # Здесь будет логика получения чатов
    pass

@router.post("/{chat_id}/messages", response_model=Message)
def create_message(
    chat_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new message in chat."""
    # Здесь будет логика создания сообщения
    pass

@router.get("/{chat_id}/messages", response_model=List[Message])
def get_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages in chat."""
    # Здесь будет логика получения сообщений
    pass 
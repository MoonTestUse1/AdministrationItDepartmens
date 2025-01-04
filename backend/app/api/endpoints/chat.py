from fastapi import APIRouter, Depends, HTTPException, WebSocket, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import aiofiles
import uuid

from app.database import get_db
from app.models.user import User
from app.core.auth import get_current_user
from app.schemas.chat import Chat, Message, ChatFile
from app.websockets.chat import handle_chat_connection

router = APIRouter()

# Путь для сохранения файлов
UPLOAD_DIR = "uploads/chat_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await handle_chat_connection(websocket, db)

@router.post("/files/")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Генерируем уникальное имя файла
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Сохраняем файл
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        return {
            "filename": file.filename,
            "saved_path": file_path,
            "size": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/messages/", response_model=List[Message])
def get_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Получаем чат пользователя
    chat = db.query(Chat).filter(
        (Chat.employee_id == current_user.id) |
        (Chat.admin_id == current_user.id)
    ).first()

    if not chat:
        return []

    # Получаем сообщения
    messages = db.query(Message).filter(Message.chat_id == chat.id).all()
    return messages

@router.get("/messages/{chat_id}/", response_model=List[Message])
def get_chat_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Проверяем доступ к чату
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if not current_user.is_admin and chat.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Получаем сообщения
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    return messages

@router.get("/unread-count/")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Получаем чат пользователя
    chat = db.query(Chat).filter(
        (Chat.employee_id == current_user.id) |
        (Chat.admin_id == current_user.id)
    ).first()

    if not chat:
        return {"unread_count": 0}

    # Считаем непрочитанные сообщения
    unread_count = db.query(Message).filter(
        Message.chat_id == chat.id,
        Message.sender_id != current_user.id,
        Message.is_read == False
    ).count()

    return {"unread_count": unread_count}

@router.get("/admin/chats/", response_model=List[Chat])
def get_admin_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Получаем все чаты с последними сообщениями и количеством непрочитанных
    chats = db.query(Chat).all()
    
    # Для каждого чата добавляем дополнительную информацию
    for chat in chats:
        # Последнее сообщение
        last_message = db.query(Message)\
            .filter(Message.chat_id == chat.id)\
            .order_by(Message.created_at.desc())\
            .first()
        chat.last_message = last_message

        # Количество непрочитанных сообщений
        unread_count = db.query(Message)\
            .filter(
                Message.chat_id == chat.id,
                Message.sender_id != current_user.id,
                Message.is_read == False
            ).count()
        chat.unread_count = unread_count

    return chats 
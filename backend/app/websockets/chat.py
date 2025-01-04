from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List, Optional
from datetime import datetime
import json

from app.core.auth import get_current_user_ws
from app.models.user import User
from app.models.chat import Chat, Message, ChatFile
from app.database import get_db
from sqlalchemy.orm import Session

class ConnectionManager:
    def __init__(self):
        # Хранение активных соединений: {user_id: WebSocket}
        self.active_connections: Dict[int, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            
    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)
            
    def is_connected(self, user_id: int) -> bool:
        return user_id in self.active_connections

manager = ConnectionManager()

async def handle_chat_connection(
    websocket: WebSocket,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_ws)
):
    await manager.connect(websocket, current_user.id)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Обработка различных типов сообщений
            message_type = data.get('type')
            
            if message_type == 'message':
                # Создание нового сообщения
                chat = db.query(Chat).filter(
                    (Chat.employee_id == current_user.id) |
                    (Chat.admin_id == current_user.id)
                ).first()
                
                if not chat:
                    # Создаем новый чат для сотрудника
                    admin = db.query(User).filter(User.is_admin == True).first()
                    chat = Chat(employee_id=current_user.id, admin_id=admin.id)
                    db.add(chat)
                    db.commit()
                
                message = Message(
                    chat_id=chat.id,
                    sender_id=current_user.id,
                    content=data['content']
                )
                db.add(message)
                db.commit()
                
                # Определяем получателя
                recipient_id = chat.admin_id if current_user.id == chat.employee_id else chat.employee_id
                
                # Отправляем сообщение получателю
                message_data = {
                    'type': 'message',
                    'id': message.id,
                    'sender_id': current_user.id,
                    'content': message.content,
                    'created_at': message.created_at.isoformat(),
                    'is_read': False
                }
                
                if manager.is_connected(recipient_id):
                    await manager.send_personal_message(message_data, recipient_id)
                
            elif message_type == 'read':
                # Отмечаем сообщения как прочитанные
                message_ids = data.get('message_ids', [])
                db.query(Message).filter(Message.id.in_(message_ids)).update(
                    {Message.is_read: True},
                    synchronize_session=False
                )
                db.commit()
                
                # Отправляем подтверждение прочтения
                chat = db.query(Chat).filter(
                    (Chat.employee_id == current_user.id) |
                    (Chat.admin_id == current_user.id)
                ).first()
                
                if chat:
                    recipient_id = chat.admin_id if current_user.id == chat.employee_id else chat.employee_id
                    if manager.is_connected(recipient_id):
                        await manager.send_personal_message({
                            'type': 'read_confirmation',
                            'message_ids': message_ids
                        }, recipient_id)
            
    except WebSocketDisconnect:
        manager.disconnect(current_user.id)
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")
        manager.disconnect(current_user.id) 
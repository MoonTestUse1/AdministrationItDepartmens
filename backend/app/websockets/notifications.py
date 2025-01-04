from fastapi import WebSocket
from typing import Dict, List
import json

class NotificationManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "admin": [],  # Подключения админов
            "employee": []  # Подключения сотрудников
        }

    async def connect(self, websocket: WebSocket, client_type: str):
        await websocket.accept()
        self.active_connections[client_type].append(websocket)

    def disconnect(self, websocket: WebSocket, client_type: str):
        self.active_connections[client_type].remove(websocket)

    async def broadcast_to_admins(self, message: dict):
        """Отправка сообщения всем подключенным админам"""
        for connection in self.active_connections["admin"]:
            try:
                await connection.send_json(message)
            except:
                # Если не удалось отправить сообщение, пропускаем
                continue

    async def broadcast_to_employees(self, employee_id: int, message: dict):
        """Отправка сообщения конкретному сотруднику"""
        for connection in self.active_connections["employee"]:
            try:
                await connection.send_json(message)
            except:
                continue

notification_manager = NotificationManager() 
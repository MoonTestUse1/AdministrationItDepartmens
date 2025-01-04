from fastapi import WebSocket
from typing import Dict, List
import json
import logging

logger = logging.getLogger(__name__)

class NotificationManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "admin": [],  # Подключения админов
            "employee": []  # Подключения сотрудников
        }

    async def connect(self, websocket: WebSocket, client_type: str):
        await websocket.accept()
        self.active_connections[client_type].append(websocket)
        logger.info(f"New {client_type} connection. Total connections: {len(self.active_connections[client_type])}")

    def disconnect(self, websocket: WebSocket, client_type: str):
        if websocket in self.active_connections[client_type]:
            self.active_connections[client_type].remove(websocket)
            logger.info(f"{client_type} disconnected. Remaining connections: {len(self.active_connections[client_type])}")

    async def broadcast_to_admins(self, message: dict):
        """Отправка сообщения всем подключенным админам"""
        logger.info(f"Broadcasting to admins: {message}")
        disconnected = []
        
        for connection in self.active_connections["admin"]:
            try:
                await connection.send_json(message)
                logger.info("Message sent successfully")
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                disconnected.append(connection)
                continue
        
        # Удаляем отключенные соединения
        for connection in disconnected:
            self.disconnect(connection, "admin")

    async def broadcast_to_employees(self, employee_id: int, message: dict):
        """Отправка сообщения конкретному сотруднику"""
        logger.info(f"Broadcasting to employee {employee_id}: {message}")
        disconnected = []
        
        for connection in self.active_connections["employee"]:
            try:
                await connection.send_json(message)
                logger.info("Message sent successfully")
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                disconnected.append(connection)
                continue
        
        # Удаляем отключенные соединения
        for connection in disconnected:
            self.disconnect(connection, "employee")

notification_manager = NotificationManager() 
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
        logger.info(f"Number of admin connections: {len(self.active_connections['admin'])}")
        
        if not self.active_connections["admin"]:
            logger.warning("No admin connections available")
            return
            
        disconnected = []
        
        for connection in self.active_connections["admin"]:
            try:
                await connection.send_json(message)
                logger.info("Message sent successfully to admin")
            except Exception as e:
                logger.error(f"Error sending message to admin: {e}")
                disconnected.append(connection)
                continue
        
        # Удаляем отключенные соединения
        for connection in disconnected:
            self.disconnect(connection, "admin")

    async def broadcast_to_employees(self, employee_id: int, message: dict):
        """Отправка сообщения конкретному сотруднику"""
        logger.info(f"Broadcasting to employee {employee_id}: {message}")
        logger.info(f"Number of employee connections: {len(self.active_connections['employee'])}")
        
        if not self.active_connections["employee"]:
            logger.warning("No employee connections available")
            return
            
        disconnected = []
        
        for connection in self.active_connections["employee"]:
            try:
                await connection.send_json(message)
                logger.info("Message sent successfully to employee")
            except Exception as e:
                logger.error(f"Error sending message to employee: {e}")
                disconnected.append(connection)
                continue
        
        # Удаляем отключенные соединения
        for connection in disconnected:
            self.disconnect(connection, "employee")

    async def handle_ping(self, websocket: WebSocket):
        """Обработка ping сообщений"""
        try:
            await websocket.send_json({"type": "pong"})
            logger.debug("Sent pong response")
        except Exception as e:
            logger.error(f"Error sending pong: {e}")

notification_manager = NotificationManager() 
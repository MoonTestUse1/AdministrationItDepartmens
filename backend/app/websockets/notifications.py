"""WebSocket notifications manager"""
from fastapi import WebSocket
from typing import Dict, List, Set
import logging
import json

logger = logging.getLogger(__name__)

class NotificationManager:
    """Менеджер WebSocket подключений и уведомлений"""
    def __init__(self):
        self.admin_connections: Set[WebSocket] = set()
        self.employee_connections: Dict[int, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, client_type: str, employee_id: int = None):
        """Установка WebSocket соединения"""
        await websocket.accept()
        if client_type == "admin":
            self.admin_connections.add(websocket)
            logger.info("Admin connected to WebSocket")
        elif client_type == "employee" and employee_id:
            self.employee_connections[employee_id] = websocket
            logger.info(f"Employee {employee_id} connected to WebSocket")

    def disconnect(self, websocket: WebSocket, client_type: str, employee_id: int = None):
        """Закрытие WebSocket соединения"""
        if client_type == "admin":
            self.admin_connections.discard(websocket)
            logger.info("Admin disconnected from WebSocket")
        elif client_type == "employee" and employee_id:
            self.employee_connections.pop(employee_id, None)
            logger.info(f"Employee {employee_id} disconnected from WebSocket")

    async def broadcast_to_admins(self, message: dict):
        """Отправка сообщения всем админам"""
        disconnected = set()
        for websocket in self.admin_connections:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to admin: {e}")
                disconnected.add(websocket)
        
        # Удаляем отключенные соединения
        for websocket in disconnected:
            self.disconnect(websocket, "admin")

    async def send_to_employee(self, employee_id: int, message: dict):
        """Отправка сообщения конкретному сотруднику"""
        websocket = self.employee_connections.get(employee_id)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to employee {employee_id}: {e}")
                self.disconnect(websocket, "employee", employee_id)

    async def handle_ping(self, websocket: WebSocket):
        """Обработка ping-сообщений"""
        try:
            await websocket.send_json({"type": "pong"})
        except Exception as e:
            logger.error(f"Error handling ping: {e}")

    async def admin_endpoint(self, websocket: WebSocket):
        """WebSocket endpoint для админов"""
        await self.connect(websocket, "admin")
        try:
            while True:
                data = await websocket.receive_json()
                if data.get("type") == "ping":
                    await self.handle_ping(websocket)
        except Exception as e:
            logger.error(f"Error in admin websocket: {e}")
        finally:
            self.disconnect(websocket, "admin")

    async def employee_endpoint(self, websocket: WebSocket, employee_id: int):
        """WebSocket endpoint для сотрудников"""
        await self.connect(websocket, "employee", employee_id)
        try:
            while True:
                data = await websocket.receive_json()
                if data.get("type") == "ping":
                    await self.handle_ping(websocket)
        except Exception as e:
            logger.error(f"Error in employee websocket: {e}")
        finally:
            self.disconnect(websocket, "employee", employee_id)


# Создаем глобальный экземпляр менеджера уведомлений
notification_manager = NotificationManager() 
from typing import Optional
from fastapi import WebSocket, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User

async def get_current_user_ws(websocket: WebSocket, db: Session) -> Optional[User]:
    """Get current user from WebSocket connection."""
    try:
        # Получаем токен из параметров запроса
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        # Проверяем токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        # Получаем пользователя
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        return user

    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None 
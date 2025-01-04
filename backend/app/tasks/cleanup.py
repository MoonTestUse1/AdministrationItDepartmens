import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.chat import Message, ChatFile

def cleanup_old_messages():
    """Удаляет сообщения и файлы старше 1 месяца"""
    db = SessionLocal()
    try:
        # Определяем дату, до которой нужно удалить сообщения
        cutoff_date = datetime.utcnow() - timedelta(days=30)

        # Получаем файлы, которые нужно удалить
        files_to_delete = db.query(ChatFile)\
            .join(Message)\
            .filter(Message.created_at < cutoff_date)\
            .all()

        # Удаляем физические файлы
        for file in files_to_delete:
            try:
                if os.path.exists(file.file_path):
                    os.remove(file.file_path)
            except Exception as e:
                print(f"Error deleting file {file.file_path}: {e}")

        # Удаляем старые сообщения (каскадно удалятся и записи о файлах)
        db.query(Message)\
            .filter(Message.created_at < cutoff_date)\
            .delete(synchronize_session=False)

        db.commit()
    except Exception as e:
        print(f"Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close() 
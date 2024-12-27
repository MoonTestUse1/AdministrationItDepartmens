"""Handlers for callback queries"""
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session
from ...database import get_db
from ... import models
from ..config import RequestStatus

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith('status_'))
async def process_status_button(callback_query: types.CallbackQuery):
    """
    Handle status update button clicks.
    Updates request status in database and updates message in Telegram.
    """
    try:
        # Parse callback data
        _, request_id, new_status = callback_query.data.split('_')
        request_id = int(request_id)
        
        # Get database session
        db = next(get_db())
        
        # Update request status
        request = db.query(models.Request).filter(models.Request.id == request_id).first()
        if request:
            request.status = new_status
            db.commit()
            
            # Update message in Telegram
            await callback_query.message.edit_text(
                f"Заявка №{request_id}\n"
                f"Статус: {new_status}\n"
                f"Описание: {request.description}",
                reply_markup=get_updated_keyboard(request_id, new_status)
            )
            
            await callback_query.answer("Статус успешно обновлен!")
        else:
            await callback_query.answer("Заявка не найдена!", show_alert=True)
            
    except Exception as e:
        print(f"Error in process_status_button: {e}")
        await callback_query.answer(
            "Произошла ошибка при обновлении статуса",
            show_alert=True
        )

def get_updated_keyboard(request_id: int, current_status: str) -> InlineKeyboardMarkup:
    """Create keyboard with status update buttons"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    if current_status != RequestStatus.IN_PROGRESS:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="В работе",
                callback_data=f"status_{request_id}_{RequestStatus.IN_PROGRESS}"
            )
        ])
    
    if current_status != RequestStatus.COMPLETED:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="Завершено",
                callback_data=f"status_{request_id}_{RequestStatus.COMPLETED}"
            )
        ])
    
    return keyboard
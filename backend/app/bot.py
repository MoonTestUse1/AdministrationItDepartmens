from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

# Создаем роутер для обработки callback'ов
from aiogram import Router
router = Router()

# Обработчик нажатия кнопки
@router.callback_query(lambda c: c.data.startswith('status_'))
async def process_status_button(callback_query: types.CallbackQuery):
    try:
        print(f"Hello world: {callback_query.data}")
        # Получаем ID заявки и новый статус из callback_data
        _, request_id, new_status = callback_query.data.split('_')
        request_id = int(request_id)
        
        # Получаем сессию базы данных
        db = next(get_db())
        
        # Обновляем статус в базе данных
        request = db.query(models.Request).filter(models.Request.id == request_id).first()
        if request:
            request.status = new_status
            db.commit()
            
            # Обновляем сообщение в боте
            await callback_query.message.edit_text(
                f"Заявка №{request_id}\nСтатус: {new_status}",
                reply_markup=get_updated_keyboard(request_id, new_status)
            )
            
            # Отправляем уведомление о успешном обновлении
            await callback_query.answer("Статус успешно обновлен!")
        else:
            await callback_query.answer("Заявка не найдена!", show_alert=True)
            
    except Exception as e:
        print(f"Error in process_status_button: {e}")
        await callback_query.answer("Произошла ошибка при обновлении статуса", show_alert=True)

def get_updated_keyboard(request_id: int, current_status: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    if current_status != "in_progress":
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="В работе", 
                callback_data=f"status_{request_id}_in_progress"
            )
        ])
    
    if current_status != "completed":
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="Завершено", 
                callback_data=f"status_{request_id}_completed"
            )
        ])
    
    return keyboard

# В основном файле бота (где создается диспетчер)
dp = Dispatcher()
dp.include_router(router)
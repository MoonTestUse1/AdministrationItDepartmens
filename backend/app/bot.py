# from logging import getLogger
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import CommandStart
# from sqlalchemy.orm import Session
# from .database import get_db
# from .crud import requests
# from .utils.telegram import STATUS_LABELS, create_status_keyboard, format_request_message

# # Initialize logger
# logger = getLogger(__name__)

# # Initialize bot and dispatcher
# bot = Bot(token="7677506032:AAHEqNUr1lIUfNVbLwaWIaPeKKShsCyz3eo")
# dp = Dispatcher()

# @dp.callback_query(lambda c: c.data and c.data.startswith('status_'))
# async def process_status_update(callback: types.CallbackQuery):
#     """Handle status update button clicks"""
#     try:
#         # Parse callback data using underscore as separator
#         parts = callback.data.split('_')
#         logger.info(f"Parsed callback parts: {parts}")

#         if len(parts) < 3:
#             logger.warning(f"Invalid callback data format: {parts}")
#             return

#         request_id = int(parts[1])
#         # Handle 'in_progress' case where we have an extra underscore
#         new_status = '_'.join(parts[2:]) if len(parts) > 3 else parts[2]

#         logger.info(f"Processing status update: request_id={request_id}, new_status={new_status}")

#         # Get database session
#         db = next(get_db())

#         try:
#             # Update request status in database
#             updated_request = requests.update_request_status(db, request_id, new_status)
#             if not updated_request:
#                 logger.warning(f"Request not found: {request_id}")
#                 await callback.answer("Заявка не найдена", show_alert=True)
#                 return

#             # Update message with new status
#             new_message = format_request_message(updated_request)
#             new_keyboard = create_status_keyboard(request_id, new_status)

#             await callback.message.edit_text(
#                 text=new_message,
#                 parse_mode="HTML",
#                 reply_markup=new_keyboard
#             )

#             await callback.answer(f"Статус обновлен: {STATUS_LABELS[new_status]}")
#             logger.info(f"Successfully updated request {request_id} to status {new_status}")

#         except ValueError as e:
#             logger.error(f"Value error while updating status: {e}")
#             await callback.answer(str(e), show_alert=True)
#         finally:
#             db.close()

#     except Exception as e:
#         logger.error(f"Error processing callback: {e}", exc_info=True)
#         await callback.answer("Произошла ошибка при обновлении статуса", show_alert=True)

# @dp.message(CommandStart())
# async def start_command(message: types.Message):
#     """Handle /start command"""
#     await message.answer(
#         "👋 Привет! Я бот технической поддержки.\n"
#         "Я буду отправлять уведомления о новых заявках и позволю менять их статус."
#     )

# async def start_bot():
#     """Start the bot"""
#     try:
#         await dp.start_polling(bot)
#     finally:
#         await bot.session.close()

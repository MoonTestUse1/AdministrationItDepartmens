from aiogram import types, F
from logging import getLogger
from sqlalchemy.orm import Session
from ...database import get_db
from ...crud import requests
from ..bot import dp
from ..keyboards import create_status_keyboard
from ..messages import format_request_message
from ..constants import STATUS_LABELS

logger = getLogger(__name__)

@dp.callback_query(F.data.startswith("status_"))
async def process_status_update(callback: types.CallbackQuery):
    try:
        parts = callback.data.split("_")
        logger.info(f"Received callback data: {callback.data}")

        if len(parts) < 3:
            logger.error(f"Invalid callback data format: {parts}")
            await callback.answer("Неверный формат данных", show_alert=True)
            return

        request_id = int(parts[1])
        new_status = "_".join(parts[2:]) if len(parts) > 3 else parts[2]

        logger.info(
            f"Processing status update: request_id={request_id}, new_status={new_status}"
        )

        db = next(get_db())
        try:
            updated_request = requests.update_request_status(db, request_id, new_status)
            if not updated_request:
                logger.warning(f"Request not found: {request_id}")
                await callback.answer("Заявка не найдена", show_alert=True)
                return

            new_message = format_request_message(updated_request)
            new_keyboard = create_status_keyboard(request_id, new_status)

            await callback.message.edit_text(
                text=new_message, parse_mode="HTML", reply_markup=new_keyboard
            )

            await callback.answer(f"Статус обновлен: {STATUS_LABELS[new_status]}")
            logger.info(
                f"Successfully updated request {request_id} to status {new_status}"
            )

        except ValueError as e:
            logger.error(f"Value error while updating status: {e}")
            await callback.answer(str(e), show_alert=True)
        finally:
            db.close()

    except Exception as e:
        logger.error(f"Error processing callback: {e}", exc_info=True)
        await callback.answer(
            "Произошла ошибка при обновлении статуса", show_alert=True
        )

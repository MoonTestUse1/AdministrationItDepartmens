from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from logging import getLogger
from .constants import STATUS_LABELS

logger = getLogger(__name__)

def create_status_keyboard(
    request_id: int, current_status: str
) -> InlineKeyboardMarkup:
    status_transitions = {
        "new": ["in_progress"],
        "in_progress": ["resolved"],
        "resolved": ["closed"],
        "closed": [],
    }

    buttons = []
    available_statuses = status_transitions.get(current_status, [])

    for status in available_statuses:
        callback_data = f"status_{request_id}_{status}"
        logger.debug(f"Creating button with callback_data: {callback_data}")
        buttons.append(
            [
                InlineKeyboardButton(
                    text=STATUS_LABELS[status], callback_data=callback_data
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    logger.debug(f"Created keyboard: {keyboard}")
    return keyboard

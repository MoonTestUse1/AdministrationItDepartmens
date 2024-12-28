from datetime import datetime
from .constants import (
    STATUS_LABELS,
    PRIORITY_LABELS,
    PRIORITY_EMOJI,
    DEPARTMENT_LABELS,
    REQUEST_TYPE_LABELS,
    REQUEST_TYPE_EMOJI,
)


def format_request_message(request_data: dict) -> str:
    created_at = datetime.fromisoformat(request_data["created_at"]).strftime(
        "%d.%m.%Y %H:%M"
    )

    # Get translated values
    department = DEPARTMENT_LABELS.get(
        request_data["department"], request_data["department"]
    )
    request_type = REQUEST_TYPE_LABELS.get(
        request_data["request_type"], request_data["request_type"]
    )
    priority = PRIORITY_LABELS.get(request_data["priority"], request_data["priority"])
    status = STATUS_LABELS.get(request_data.get("status", "new"), "Неизвестно")

    return (
        f"📋 <b>Заявка #{request_data['id']}</b>\n\n"
        f"👤 <b>Сотрудник:</b> {request_data['employee_last_name']} {request_data['employee_first_name']}\n"
        f"🏢 <b>Отдел:</b> {department}\n"
        f"🚪 <b>Кабинет:</b> {request_data['office']}\n"
        f"{REQUEST_TYPE_EMOJI.get(request_data['request_type'], '📝')} <b>Тип заявки:</b> {request_type}\n"
        f"{PRIORITY_EMOJI.get(request_data['priority'], '⚪')} <b>Приоритет:</b> {priority}\n\n"
        f"📝 <b>Описание:</b>\n<blockquote>{request_data['description']}</blockquote>\n\n"
        f"🕒 <b>Создана:</b> {created_at}\n"
        f"📊 <b>Статус:</b> {status}"
    )

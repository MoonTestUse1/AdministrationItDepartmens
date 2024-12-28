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
        f"📋 Заявка #{request_data['id']}\n\n"
        f"👤 Сотрудник: {request_data['employee_last_name']} {request_data['employee_first_name']}\n"
        f"🏢 Отдел: {department}\n"
        f"🚪 Кабинет: {request_data['office']}\n"
        f"{REQUEST_TYPE_EMOJI.get(request_data['request_type'], '📝')} Тип заявки: {request_type}\n"
        f"{PRIORITY_EMOJI.get(request_data['priority'], '⚪')} Приоритет: {priority}\n\n"
        f"📝 Описание:\n{request_data['description']}\n\n"
        f"🕒 Создана: {created_at}\n"
        f"📊 Статус: {status}"
    )


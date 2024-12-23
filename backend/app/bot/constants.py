from enum import Enum


class RequestStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class RequestPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Department(str, Enum):
    AHO = "aho"
    GKH = "gkh"
    GENERAL = "general"


class RequestType(str, Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK = "network"
    ACCESS = "access"
    OTHER = "other"


STATUS_LABELS = {
    RequestStatus.NEW: "Новая",
    RequestStatus.IN_PROGRESS: "В работе",
    RequestStatus.RESOLVED: "Решена",
    RequestStatus.CLOSED: "Закрыта",
}

PRIORITY_LABELS = {
    RequestPriority.LOW: "Низкий",
    RequestPriority.MEDIUM: "Средний",
    RequestPriority.HIGH: "Высокий",
    RequestPriority.CRITICAL: "Критический",
}

PRIORITY_EMOJI = {
    RequestPriority.LOW: "🟢",
    RequestPriority.MEDIUM: "🟡",
    RequestPriority.HIGH: "🟠",
    RequestPriority.CRITICAL: "🔴",
}

DEPARTMENT_LABELS = {
    Department.AHO: "Административно-хозяйственный отдел",
    Department.GKH: "Жилищно-коммунальное хозяйство",
    Department.GENERAL: "Общий отдел",
}

REQUEST_TYPE_LABELS = {
    RequestType.HARDWARE: "Проблемы с оборудованием",
    RequestType.SOFTWARE: "Проблемы с ПО",
    RequestType.NETWORK: "Проблемы с сетью",
    RequestType.ACCESS: "Доступ к системам",
    RequestType.OTHER: "Другое",
}

REQUEST_TYPE_EMOJI = {
    RequestType.HARDWARE: "🖥️",
    RequestType.SOFTWARE: "💿",
    RequestType.NETWORK: "🌐",
    RequestType.ACCESS: "🔑",
    RequestType.OTHER: "📝",
}

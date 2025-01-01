const STATUS_LABELS: Record<string, string> = {
    new: 'Новая',
    in_progress: 'В работе',
    resolved: 'Решена',
    closed: 'Закрыта'
  };
  
  const REQUEST_TYPE_LABELS: Record<string, string> = {
    hardware: 'Проблемы с оборудованием',
    software: 'Проблемы с ПО',
    network: 'Проблемы с сетью',
    access: 'Доступ к системам',
    other: 'Другое'
  };
  
  export const getStatusLabel = (status: string): string => {
    return STATUS_LABELS[status] || status;
  };
  
  export const getRequestTypeLabel = (type: string): string => {
    return REQUEST_TYPE_LABELS[type] || type;
  };
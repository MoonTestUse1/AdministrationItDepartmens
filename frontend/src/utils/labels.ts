export const getRequestTypeLabel = (type: string): string => {
  const types: Record<string, string> = {
    hardware: 'Оборудование',
    software: 'Программное обеспечение',
    network: 'Сеть',
    access: 'Доступ',
    other: 'Другое'
  };
  return types[type] || type;
};

export const getStatusLabel = (status: string): string => {
  const statuses: Record<string, string> = {
    new: 'Новая',
    in_progress: 'В работе',
    resolved: 'Решена',
    closed: 'Закрыта'
  };
  return statuses[status] || status;
};
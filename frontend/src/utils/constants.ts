export const departments = [
  { value: 'aho', label: 'Административно-хозяйственный отдел' },
  { value: 'gkh', label: 'Жилищно-коммунальное хозяйство' },
  { value: 'general', label: 'Общий отдел' }
] as const;

export const requestTypes = [
  { value: 'hardware', label: 'Проблемы с оборудованием' },
  { value: 'software', label: 'Проблемы с программным обеспечением' },
  { value: 'network', label: 'Проблемы с сетью' },
  { value: 'access', label: 'Доступ к системам' },
  { value: 'other', label: 'Другое' }
] as const;

export function getRequestTypeLabel(value: string): string {
  return requestTypes.find(type => type.value === value)?.label || value;
}
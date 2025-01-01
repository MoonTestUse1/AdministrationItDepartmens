import { ref, computed } from 'vue';
import type { Statistics, StatisticCard } from '@/types/statistics';

export function useStatistics() {
  const statistics = ref<Statistics | null>(null);

  const statisticsCards = computed<StatisticCard[]>(() => {
    if (!statistics.value) return [];
    return [
      { period: 'total', label: 'Всего заявок', value: statistics.value.totalRequests },
      { period: 'resolved', label: 'Решено', value: statistics.value.resolvedRequests },
      { period: 'avgTime', label: 'Среднее время', value: statistics.value.averageResolutionTime }
    ];
  });

  const fetchStatistics = async () => {
    try {
      const response = await fetch('/api/admin/statistics?period=week');
      if (!response.ok) throw new Error('Failed to fetch statistics');
      statistics.value = await response.json();
    } catch (error) {
      console.error('Error fetching statistics:', error);
    }
  };

  return {
    statistics,
    statisticsCards,
    fetchStatistics
  };
}
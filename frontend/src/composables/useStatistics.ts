import { ref } from 'vue';

interface StatisticCard {
  period: string;
  label: string;
  value: number | string;
}

export function useStatistics() {
  const statisticsCards = ref<StatisticCard[]>([]);

  const fetchStatistics = async () => {
    try {
      const response = await fetch('/api/admin/statistics?period=week');
      if (!response.ok) throw new Error('Failed to fetch statistics');
      const data = await response.json();
      statisticsCards.value = [
        { period: 'total', label: 'Всего заявок', value: data.totalRequests },
        { period: 'resolved', label: 'Решено', value: data.resolvedRequests },
        { period: 'avgTime', label: 'Среднее время', value: data.averageResolutionTime }
      ];
    } catch (error) {
      console.error('Error fetching statistics:', error);
    }
  };

  return {
    statisticsCards,
    fetchStatistics
  };
}
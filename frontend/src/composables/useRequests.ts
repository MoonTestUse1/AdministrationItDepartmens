import { ref } from 'vue';
import type { Request } from '@/types/request';

export function useRequests() {
  const requests = ref<Request[]>([]);

  const fetchRequests = async () => {
    try {
      const response = await fetch('/api/admin/requests');
      if (!response.ok) throw new Error('Failed to fetch requests');
      requests.value = await response.json();
    } catch (error) {
      console.error('Error fetching requests:', error);
    }
  };

  return {
    requests,
    fetchRequests
  };
}
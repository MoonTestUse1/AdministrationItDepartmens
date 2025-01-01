import { ref } from 'vue';

interface Request {
  id: number;
  employee_last_name: string;
  request_type: string;
  status: string;
  created_at: string;
}

export function useRequests() {
  const requests = ref<Request[]>([]);

  const fetchRequests = async () => {
    try {
      const response = await fetch('/api/requests/');
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
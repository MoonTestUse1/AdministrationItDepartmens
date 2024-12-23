export type RequestStatus = 'new' | 'in_progress' | 'resolved' | 'closed';

export interface Request {
    id: number;
    status: RequestStatus;
    created_at: string;
    employee_last_name: string;
    employee_first_name: string;
    employee_office: string;
    request_type: string;
    priority: 'low' | 'medium' | 'high' | 'critical';
    description: string;
  }
  
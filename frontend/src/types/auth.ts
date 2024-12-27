export interface User {
  id: string;
  firstName: string;
  lastName: string;
  department: string;
  createdAt: string;
}

export interface LoginCredentials {
  lastName: string;
  password: string;
}

export interface AdminCredentials {
  username: string;
  password: string;
}

export interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  department: string;
  office: string;
}

export interface Request {
  id: number;
  employee_last_name: string;
  employee_first_name: string;
  employee_office: string;
  request_type: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'new' | 'in_progress' | 'resolved' | 'closed';
  created_at: string;
}
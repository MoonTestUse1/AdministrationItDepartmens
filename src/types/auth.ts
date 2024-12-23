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
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

interface LoginResponse {
  access_token: string
  token_type: string
  [key: string]: any
}

interface Employee {
  id: number
  first_name: string
  last_name: string
  department: string
  office: string
  position: string
  created_at: string
}

interface Request {
  id: number
  employee: Employee
  department: string
  request_type: string
  priority: 'low' | 'medium' | 'high' | 'critical'
  description: string
  status: 'new' | 'in_progress' | 'resolved'
  created_at: string
}

interface Statistics {
  new: number
  inProgress: number
  resolved: number
}

interface EmployeeForm {
  id: number | null
  first_name: string
  last_name: string
  department: string
  office: string
  position: string
  password: string
} 
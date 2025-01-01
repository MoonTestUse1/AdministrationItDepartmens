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
  created_at: string
}

interface Request {
  id: number
  employee_id: number
  department: string
  request_type: string
  priority: string
  description: string
  status: string
  created_at: string
} 
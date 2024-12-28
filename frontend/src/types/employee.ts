export interface Employee {
    id: number;
    first_name: string;
    last_name: string;
    department: string;
    office: string;
    created_at?: string;
  }

  export interface EmployeeFormData {
    first_name: string;
    last_name: string;
    department: string;
    office: string;
    password?: string; // Делаем password опциональным
  }
  
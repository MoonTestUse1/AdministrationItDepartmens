/*
  # Add Employee Creation Function
  
  1. Changes
    - Add secure function to create new employees with password hashing
  
  2. Security
    - Uses hash_password function for secure password storage
    - SECURITY DEFINER to ensure proper access control
    - Returns employee data without password hash
*/

-- Create function to create employee with password
CREATE OR REPLACE FUNCTION create_employee(
  p_first_name text,
  p_last_name text,
  p_department text,
  p_password text
)
RETURNS employees
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_employee employees;
BEGIN
  -- Validate input
  IF p_password IS NULL OR length(p_password) < 6 THEN
    RAISE EXCEPTION 'Password must be at least 6 characters long';
  END IF;

  -- Create employee with hashed password
  INSERT INTO employees (
    first_name,
    last_name,
    department,
    password_hash
  ) VALUES (
    p_first_name,
    p_last_name,
    p_department,
    hash_password(p_password)
  )
  RETURNING * INTO v_employee;
  
  -- Return employee data without password hash
  v_employee.password_hash := NULL;
  RETURN v_employee;
END;
$$;
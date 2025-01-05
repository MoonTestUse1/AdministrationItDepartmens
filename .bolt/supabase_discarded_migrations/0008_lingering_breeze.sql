/*
  # Remove email dependency from employees table

  1. Changes
    - Remove email column from employees table
    - Update create_employee function to work without email
    - Preserve existing data integrity

  2. Security
    - Maintain existing RLS policies
*/

-- Remove email column and its constraint
ALTER TABLE employees 
DROP COLUMN IF EXISTS email;

-- Update create_employee function
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
  -- Input validation
  IF p_first_name IS NULL OR p_first_name = '' THEN
    RAISE EXCEPTION 'First name is required';
  END IF;
  
  IF p_last_name IS NULL OR p_last_name = '' THEN
    RAISE EXCEPTION 'Last name is required';
  END IF;
  
  IF p_department IS NULL OR p_department = '' THEN
    RAISE EXCEPTION 'Department is required';
  END IF;
  
  IF p_password IS NULL OR length(p_password) < 6 THEN
    RAISE EXCEPTION 'Password must be at least 6 characters long';
  END IF;

  -- Create employee record
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

  RETURN v_employee;
EXCEPTION
  WHEN others THEN
    RAISE EXCEPTION 'Failed to create employee: %', SQLERRM;
END;
$$;
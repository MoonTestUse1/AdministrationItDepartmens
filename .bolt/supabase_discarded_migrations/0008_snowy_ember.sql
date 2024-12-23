/*
  # Fix database constraints and password validation

  1. Changes
    - Add password validation function
    - Add employee creation function with validation
    - Add indexes for performance optimization
    - Update RLS policies

  2. Security
    - Maintain RLS policies
    - Add proper validation for passwords
*/

-- Update password validation function
CREATE OR REPLACE FUNCTION validate_password(password text)
RETURNS boolean
LANGUAGE plpgsql
AS $$
BEGIN
  IF length(password) < 6 THEN
    RAISE EXCEPTION 'Password must be at least 6 characters long';
  END IF;
  RETURN true;
END;
$$;

-- Update create_employee function to use password validation
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
  -- Validate password
  PERFORM validate_password(p_password);

  -- Create employee
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
END;
$$;

-- Add indexes for better performance if they don't exist
CREATE INDEX IF NOT EXISTS idx_employees_last_name ON employees(last_name);
CREATE INDEX IF NOT EXISTS idx_support_requests_created_at ON support_requests(created_at DESC);

-- Update RLS policies for support_requests
DROP POLICY IF EXISTS "Users can create their own requests" ON support_requests;
DROP POLICY IF EXISTS "Users can view their own requests" ON support_requests;
DROP POLICY IF EXISTS "Users can update their own requests" ON support_requests;

CREATE POLICY "Employees can create their own requests"
  ON support_requests
  FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Employees can view their own requests"
  ON support_requests
  FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Employees can update their own requests"
  ON support_requests
  FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());
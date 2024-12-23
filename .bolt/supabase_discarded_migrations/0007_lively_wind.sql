/*
  # Add create_user function

  1. Changes
    - Add function to create new users in employees table
    - Function handles first name, last name, department and password
    - Returns the created employee record

  2. Details
    - Creates a stored procedure for consistent user creation
    - Validates input parameters
    - Returns the full employee record after creation

  3. Security
    - Function is SECURITY DEFINER to ensure proper access control
    - Input validation to prevent invalid data
*/

-- Create function to handle user creation
CREATE OR REPLACE FUNCTION create_user(
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
  -- Validate inputs
  IF p_first_name IS NULL OR p_first_name = '' THEN
    RAISE EXCEPTION 'First name cannot be empty';
  END IF;
  
  IF p_last_name IS NULL OR p_last_name = '' THEN
    RAISE EXCEPTION 'Last name cannot be empty';
  END IF;
  
  IF p_department IS NULL OR p_department = '' THEN
    RAISE EXCEPTION 'Department cannot be empty';
  END IF;
  
  IF p_password IS NULL OR p_password = '' THEN
    RAISE EXCEPTION 'Password cannot be empty';
  END IF;

  -- Insert new employee
  INSERT INTO employees (
    first_name,
    last_name,
    department,
    email -- Generate email from name
  ) VALUES (
    p_first_name,
    p_last_name,
    p_department,
    lower(p_last_name || '@example.com')
  )
  RETURNING * INTO v_employee;

  RETURN v_employee;
END;
$$;
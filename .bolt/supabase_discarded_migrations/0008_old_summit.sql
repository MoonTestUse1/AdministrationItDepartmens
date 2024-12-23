/*
  # Fix employee creation functions

  1. Changes
    - Drop and recreate validate_password function with correct return type
    - Update create_employee function
    
  2. Security
    - Maintain SECURITY DEFINER
    - Secure password handling
*/

-- Drop existing functions
DROP FUNCTION IF EXISTS validate_password(text);
DROP FUNCTION IF EXISTS create_employee(text, text, text, text);

-- Recreate validate_password function
CREATE OR REPLACE FUNCTION validate_password(password text)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  IF length(password) < 6 THEN
    RAISE EXCEPTION 'Password must be at least 6 characters long';
  END IF;
END;
$$;

-- Create employee function with auth integration
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
  IF p_first_name IS NULL OR p_first_name = '' THEN
    RAISE EXCEPTION 'First name is required';
  END IF;
  
  IF p_last_name IS NULL OR p_last_name = '' THEN
    RAISE EXCEPTION 'Last name is required';
  END IF;
  
  IF p_department IS NULL OR p_department = '' THEN
    RAISE EXCEPTION 'Department is required';
  END IF;

  -- Validate password
  PERFORM validate_password(p_password);

  -- Create employee record
  INSERT INTO employees (
    first_name,
    last_name,
    department,
    email,
    password_hash
  ) VALUES (
    p_first_name,
    p_last_name,
    p_department,
    lower(p_last_name) || '@example.com',
    hash_password(p_password)
  )
  RETURNING * INTO v_employee;

  RETURN v_employee;
EXCEPTION
  WHEN others THEN
    RAISE EXCEPTION 'Failed to create employee: %', SQLERRM;
END;
$$;
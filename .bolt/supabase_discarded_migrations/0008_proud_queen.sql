/*
  # Fix employee management functions

  1. Changes
    - Drop and recreate validate_password function with proper return type
    - Create improved create_employee function with better validation
    
  2. Security
    - Maintain SECURITY DEFINER for sensitive operations
    - Secure password validation and hashing
    - Input validation for all fields
*/

-- Drop existing validate_password function if it exists
DROP FUNCTION IF EXISTS validate_password(text);

-- Recreate validate_password function with better validation
CREATE OR REPLACE FUNCTION validate_password(password text)
RETURNS boolean
LANGUAGE plpgsql
AS $$
BEGIN
  -- Check password length
  IF length(password) < 6 THEN
    RETURN false;
  END IF;
  
  RETURN true;
END;
$$;

-- Create employee function with improved validation
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
  IF NOT validate_password(p_password) THEN
    RAISE EXCEPTION 'Password must be at least 6 characters long';
  END IF;

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
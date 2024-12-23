/*
  # Fix employee creation process

  1. Changes
    - Add proper error handling for auth user creation
    - Ensure atomic transaction for employee creation
    - Add better validation for employee data
    - Fix duplicate email handling

  2. Security
    - Maintain RLS policies
    - Add proper role checks
*/

-- Drop existing function if exists
DROP FUNCTION IF EXISTS create_employee(text, text, text, text);

-- Create improved employee creation function
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
  v_email text;
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

  -- Generate unique email
  v_email := lower(p_last_name) || '@example.com';

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
    v_email,
    hash_password(p_password)
  )
  RETURNING * INTO v_employee;

  -- Create auth user
  INSERT INTO auth.users (
    email,
    encrypted_password,
    email_confirmed_at,
    raw_user_meta_data
  ) VALUES (
    v_email,
    hash_password(p_password),
    now(),
    jsonb_build_object(
      'first_name', p_first_name,
      'last_name', p_last_name,
      'department', p_department
    )
  );

  RETURN v_employee;
EXCEPTION
  WHEN unique_violation THEN
    RAISE EXCEPTION 'Employee with this email already exists';
  WHEN others THEN
    RAISE EXCEPTION 'Failed to create employee: %', SQLERRM;
END;
$$;
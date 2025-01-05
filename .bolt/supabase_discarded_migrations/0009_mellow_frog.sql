/*
  # User Management Functions
  
  1. New Functions
    - User creation with password validation
    - User authentication
*/

-- Create user management function
CREATE OR REPLACE FUNCTION create_user(
  p_first_name text,
  p_last_name text,
  p_department text,
  p_password text
)
RETURNS users
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_user users;
BEGIN
  -- Validate password length
  IF length(p_password) < 4 THEN
    RAISE EXCEPTION 'Password must be at least 4 characters long';
  END IF;

  -- Create user
  INSERT INTO users (
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
  RETURNING * INTO v_user;

  RETURN v_user;
END;
$$;

-- Create authentication function
CREATE OR REPLACE FUNCTION authenticate_user(
  p_last_name text,
  p_password text
)
RETURNS TABLE (
  id uuid,
  first_name text,
  last_name text,
  department text,
  created_at timestamptz
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
  SELECT 
    u.id,
    u.first_name,
    u.last_name,
    u.department,
    u.created_at
  FROM users u
  WHERE u.last_name = p_last_name
  AND verify_password(u.password_hash, p_password);
END;
$$;
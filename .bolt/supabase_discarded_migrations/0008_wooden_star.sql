/*
  # Password Management Functions
  
  1. New Functions
    - Password hashing and verification utilities
    - Secure password management
*/

-- Create password hashing function
CREATE OR REPLACE FUNCTION hash_password(password text)
RETURNS text
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN crypt(password, gen_salt('bf'));
END;
$$;

-- Create password verification function
CREATE OR REPLACE FUNCTION verify_password(stored_hash text, password text)
RETURNS boolean
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN stored_hash = crypt(password, stored_hash);
END;
$$;
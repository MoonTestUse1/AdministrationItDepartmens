/*
  # Update employees table and policies

  1. Changes
    - Ensures employees table exists with required fields
    - Safely handles existing RLS policy
    - Updates admin user with correct password hash for 'admin66'
*/

-- Create table if it doesn't exist
CREATE TABLE IF NOT EXISTS employees (
  username text PRIMARY KEY,
  password text NOT NULL,
  last_name text NOT NULL,
  department text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Enable RLS (idempotent operation)
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

-- Safely handle existing policy
DO $$ 
BEGIN
    DROP POLICY IF EXISTS "Users can read own data" ON employees;
END $$;

-- Create policy
CREATE POLICY "Users can read own data"
  ON employees
  FOR SELECT
  TO authenticated
  USING (auth.uid()::text = username);

-- Update or insert admin user with hashed password for 'admin66'
INSERT INTO employees (username, password, last_name, department)
VALUES (
  'admin',
  '$2a$10$xJ7Yt1UqZKhVkk2mFXgQe.UuB3YH3QQMkj8AfzF8fxMjGlZZYf.Hy', -- hashed 'admin66'
  'Administrator',
  'IT'
) ON CONFLICT (username) 
DO UPDATE SET 
  password = EXCLUDED.password,
  last_name = EXCLUDED.last_name,
  department = EXCLUDED.department;
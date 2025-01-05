/*
  # Authentication System Setup

  1. Changes
    - Create employees table with all required fields
    - Add password field with NOT NULL constraint
    - Add timestamp fields for auditing
    
  2. Security
    - Enable RLS
    - Set up read and update policies
    - Add performance indexes
*/

-- Clean up and recreate employees table
CREATE TABLE IF NOT EXISTS employees (
  username text PRIMARY KEY,
  password text NOT NULL,
  last_name text NOT NULL,
  department text NOT NULL,
  last_login_timestamp timestamptz,
  created_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

-- Safely handle existing policies
DO $$ 
BEGIN
    DROP POLICY IF EXISTS "Users can read own data" ON employees;
    DROP POLICY IF EXISTS "Users can update their own data" ON employees;
END $$;

-- Create policies
CREATE POLICY "Users can read own data"
  ON employees
  FOR SELECT
  TO authenticated
  USING (auth.uid()::text = username);

CREATE POLICY "Users can update their own data"
  ON employees
  FOR UPDATE
  TO authenticated
  USING (auth.uid()::text = username)
  WITH CHECK (auth.uid()::text = username);

-- Safely handle existing indexes
DO $$ 
BEGIN
    DROP INDEX IF EXISTS idx_employees_username;
    DROP INDEX IF EXISTS idx_employees_last_login;
END $$;

-- Add indexes
CREATE INDEX idx_employees_username ON employees(username);
CREATE INDEX idx_employees_last_login ON employees(last_login_timestamp);

-- Insert admin user with hashed password for 'admin66'
INSERT INTO employees (username, password, last_name, department)
VALUES (
  'admin',
  '$2a$10$xJ7Yt1UqZKhVkk2mFXgQe.UuB3YH3QQMkj8AfzF8fxMjGlZZYf.Hy',
  'Administrator',
  'IT'
) ON CONFLICT (username) DO NOTHING;
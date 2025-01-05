/*
  # Fix Authentication Table Structure

  1. Changes
    - Recreate employees table with correct structure
    - Add proper indexes
    - Insert admin user

  2. Security
    - Enable RLS
    - Add proper policies
*/

-- Recreate the employees table with correct structure
CREATE TABLE IF NOT EXISTS employees (
  username text PRIMARY KEY,
  last_name text NOT NULL,
  department text NOT NULL,
  last_login_timestamp timestamptz,
  created_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

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

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_employees_username 
ON employees(username);

CREATE INDEX IF NOT EXISTS idx_employees_last_login 
ON employees(last_login_timestamp);

-- Insert admin user (if not exists)
INSERT INTO employees (username, last_name, department)
VALUES (
  'admin',
  'Administrator',
  'IT'
) ON CONFLICT (username) DO NOTHING;
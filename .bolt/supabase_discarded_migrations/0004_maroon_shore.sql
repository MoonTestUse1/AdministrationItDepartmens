/*
  # Update employees table and policies

  1. Changes
    - Ensures employees table exists with required fields
    - Safely handles existing RLS policy
    - Updates admin user with correct password hash
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

-- Drop existing policy if it exists
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

-- Update or insert admin user
INSERT INTO employees (username, password, last_name, department)
VALUES (
  'admin',
  '$2a$10$X4kv7j5ZcG39WgkdqhzJXO2/ZZJHNNxt0Bz4Y8DzxfBqL0Q1erqJS', -- hashed 'admin'
  'Administrator',
  'IT'
) ON CONFLICT (username) 
DO UPDATE SET 
  password = EXCLUDED.password,
  last_name = EXCLUDED.last_name,
  department = EXCLUDED.department;
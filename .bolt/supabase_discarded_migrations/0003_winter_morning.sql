/*
  # Employee Management System Schema

  1. Table Structure
    - Creates `employees` table with:
      - `username` (text, primary key)
      - `last_name` (text, not null)
      - `department` (text, not null)
      - `last_login_timestamp` (timestamptz)
      - `created_at` (timestamptz with default)

  2. Security
    - Enables Row Level Security (RLS)
    - Adds policies for:
      - Reading own data
      - Updating own data

  3. Performance
    - Adds indexes on frequently queried columns
*/

-- Drop existing table and dependencies if they exist
DROP TABLE IF EXISTS employees CASCADE;

-- Create employees table
CREATE TABLE employees (
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

-- Add performance indexes
CREATE INDEX idx_employees_username ON employees(username);
CREATE INDEX idx_employees_last_login ON employees(last_login_timestamp);

-- Insert default admin user
INSERT INTO employees (username, last_name, department)
VALUES (
  'admin',
  'Administrator',
  'IT'
) ON CONFLICT (username) DO UPDATE SET
  last_name = EXCLUDED.last_name,
  department = EXCLUDED.department;
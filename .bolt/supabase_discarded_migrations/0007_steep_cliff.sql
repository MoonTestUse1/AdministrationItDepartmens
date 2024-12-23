/*
  # Create employees and support requests tables

  1. New Tables
    - `employees`
      - `id` (uuid, primary key)
      - `first_name` (text)
      - `last_name` (text)
      - `department` (text)
      - `created_at` (timestamptz)
    - `support_requests`
      - `id` (uuid, primary key)
      - `employee_id` (uuid, foreign key)
      - `department` (text)
      - `request_type` (enum)
      - `priority` (enum)
      - `status` (enum)
      - `description` (text)
      - `created_at` (timestamptz)
      - `last_status_change` (timestamptz)

  2. Security
    - Enable RLS on both tables
    - Add appropriate policies for employees and admins
*/

-- Create enum types if they don't exist
DO $$ BEGIN
    CREATE TYPE request_type AS ENUM ('hardware', 'software', 'network', 'access', 'other');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE request_priority AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE request_status AS ENUM ('new', 'in_progress', 'resolved', 'closed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name text NOT NULL,
    last_name text NOT NULL,
    department text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

-- Enable RLS for employees
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

-- Create policies for employees
CREATE POLICY "Employees can view their own data"
    ON employees
    FOR SELECT
    TO authenticated
    USING (id = auth.uid());

CREATE POLICY "Admins can manage all employees"
    ON employees
    FOR ALL
    TO authenticated
    USING (auth.jwt() ->> 'role' = 'admin');

-- Create support requests table
CREATE TABLE IF NOT EXISTS support_requests (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id uuid REFERENCES employees(id) NOT NULL,
    department text NOT NULL,
    request_type request_type NOT NULL,
    priority request_priority NOT NULL,
    status request_status NOT NULL DEFAULT 'new',
    description text,
    created_at timestamptz NOT NULL DEFAULT now(),
    last_status_change timestamptz DEFAULT now()
);

-- Enable RLS for support requests
ALTER TABLE support_requests ENABLE ROW LEVEL SECURITY;

-- Create policies for support requests
CREATE POLICY "Employees can view their own requests"
    ON support_requests
    FOR SELECT
    TO authenticated
    USING (employee_id = auth.uid());

CREATE POLICY "Employees can create their own requests"
    ON support_requests
    FOR INSERT
    TO authenticated
    WITH CHECK (employee_id = auth.uid());

CREATE POLICY "Admins can manage all requests"
    ON support_requests
    FOR ALL
    TO authenticated
    USING (auth.jwt() ->> 'role' = 'admin');

-- Add initial test data for employees
INSERT INTO employees (first_name, last_name, department)
VALUES 
    ('Иван', 'Иванов', 'aho'),
    ('Петр', 'Петров', 'gkh'),
    ('Сергей', 'Сергеев', 'general')
ON CONFLICT (id) DO NOTHING;
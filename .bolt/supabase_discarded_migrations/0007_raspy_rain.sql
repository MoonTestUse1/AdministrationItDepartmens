/*
  # Update Employee Table RLS Policies

  1. Changes
    - Drop existing RLS policies
    - Create new policies for admin access
    - Add policy for employee self-access
  
  2. Security
    - Enable RLS on employees table
    - Admin can manage all employees
    - Employees can view their own data
*/

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Admins can manage employees" ON employees;
DROP POLICY IF EXISTS "Employees can view own data" ON employees;

-- Enable RLS
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

-- Create admin policy for full access
CREATE POLICY "Admins can manage employees"
ON employees
FOR ALL
TO authenticated
USING (
  auth.jwt() ->> 'email' = 'admin@example.com'
);

-- Create policy for employees to view their own data
CREATE POLICY "Employees can view own data"
ON employees
FOR SELECT
TO authenticated
USING (
  id = auth.uid()
);
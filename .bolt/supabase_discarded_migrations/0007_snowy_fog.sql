/*
  # Update support requests schema

  1. Changes
    - Change foreign key reference from auth.users to employees table
    - Update RLS policies to use employee_id instead of user_id
    - Add indexes for better query performance

  2. Security
    - Enable RLS
    - Add policies for employees to manage their requests
*/

-- First drop the foreign key constraint
ALTER TABLE support_requests 
  DROP CONSTRAINT IF EXISTS support_requests_user_id_fkey;

-- Then rename the column
ALTER TABLE support_requests 
  RENAME COLUMN user_id TO employee_id;

-- Add new foreign key constraint
ALTER TABLE support_requests
  ADD CONSTRAINT support_requests_employee_id_fkey 
  FOREIGN KEY (employee_id) REFERENCES employees(id);

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_support_requests_employee_id 
  ON support_requests(employee_id);

-- Update RLS policies
DROP POLICY IF EXISTS "Users can create requests" ON support_requests;
DROP POLICY IF EXISTS "Users can view their own requests" ON support_requests;
DROP POLICY IF EXISTS "Users can update their own requests" ON support_requests;
DROP POLICY IF EXISTS "IT department can manage all requests" ON support_requests;

CREATE POLICY "Employees can create requests"
  ON support_requests
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM employees
      WHERE id = support_requests.employee_id
    )
  );

CREATE POLICY "Employees can view their own requests"
  ON support_requests
  FOR SELECT
  TO authenticated
  USING (
    employee_id IN (
      SELECT id FROM employees
      WHERE id = support_requests.employee_id
    )
  );

CREATE POLICY "Employees can update their own requests"
  ON support_requests
  FOR UPDATE
  TO authenticated
  USING (
    employee_id IN (
      SELECT id FROM employees
      WHERE id = support_requests.employee_id
    )
  );
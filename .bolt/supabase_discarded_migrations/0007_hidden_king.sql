/*
  # Add employee details to support requests

  1. Changes
    - Add employee_last_name and employee_department columns to support_requests
    - Add trigger to automatically populate employee details on insert
    - Update existing records with employee details

  2. Security
    - Maintain existing RLS policies
    - No changes to security policies required as these are derived fields
*/

-- Add new columns for employee details
ALTER TABLE support_requests
ADD COLUMN IF NOT EXISTS employee_last_name text,
ADD COLUMN IF NOT EXISTS employee_department text;

-- Create function to populate employee details
CREATE OR REPLACE FUNCTION populate_employee_details()
RETURNS TRIGGER AS $$
BEGIN
  SELECT 
    last_name,
    department
  INTO
    NEW.employee_last_name,
    NEW.employee_department
  FROM employees
  WHERE id = NEW.employee_id;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop trigger if exists to avoid conflicts
DROP TRIGGER IF EXISTS set_employee_details ON support_requests;

-- Create trigger to automatically populate employee details
CREATE TRIGGER set_employee_details
  BEFORE INSERT ON support_requests
  FOR EACH ROW
  EXECUTE FUNCTION populate_employee_details();

-- Update existing records with employee details
UPDATE support_requests sr
SET 
  employee_last_name = e.last_name,
  employee_department = e.department
FROM employees e
WHERE sr.employee_id = e.id;
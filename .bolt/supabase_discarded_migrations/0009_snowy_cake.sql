/*
  # Update employees table

  1. Changes
    - Add `is_admin` column for admin access control
    - Add email generation function
    - Update existing records
*/

-- Add admin flag
ALTER TABLE employees 
ADD COLUMN IF NOT EXISTS is_admin boolean NOT NULL DEFAULT false;

-- Update existing admin users
UPDATE employees
SET is_admin = true
WHERE email LIKE '%admin%';
/*
  # Update employees table and policies
  
  1. Table Creation
    - employees
      - id (uuid, primary key)
      - first_name (text)
      - last_name (text)
      - department (text)
      - created_at (timestamptz)
  
  2. Security
    - Enable RLS
    - Add employee viewing policy (if not exists)
*/

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  first_name text NOT NULL,
  last_name text NOT NULL,
  department text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Enable RLS for employees
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

-- Safely create policy if it doesn't exist
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'employees' 
    AND policyname = 'Employees can view their own profile'
  ) THEN
    CREATE POLICY "Employees can view their own profile"
      ON employees
      FOR SELECT
      TO authenticated
      USING (id = auth.uid());
  END IF;
END $$;
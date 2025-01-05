/*
  # Create support requests table with employee relationship

  1. Changes
    - Create support_requests table with proper foreign keys
    - Add RLS policies for access control
    - Handle existing enum types safely

  2. Security
    - Enable RLS on support_requests table
    - Add policies for authenticated users and admins
*/

-- Safely create enum types if they don't exist
DO $$ BEGIN
  CREATE TYPE request_type AS ENUM ('hardware', 'software', 'network', 'access', 'other');
EXCEPTION
  WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE request_priority AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION
  WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE request_status AS ENUM ('new', 'in_progress', 'resolved', 'closed');
EXCEPTION
  WHEN duplicate_object THEN NULL;
END $$;

-- Create support requests table with proper foreign key
CREATE TABLE IF NOT EXISTS support_requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  employee_id uuid REFERENCES employees(id) ON DELETE CASCADE NOT NULL,
  department text NOT NULL,
  request_type request_type NOT NULL,
  priority request_priority NOT NULL,
  status request_status NOT NULL DEFAULT 'new',
  description text NOT NULL DEFAULT '',
  created_at timestamptz NOT NULL DEFAULT now(),
  last_status_change timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE support_requests ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view their own requests"
  ON support_requests
  FOR SELECT
  TO authenticated
  USING (employee_id = auth.uid());

CREATE POLICY "Users can create their own requests"
  ON support_requests
  FOR INSERT
  TO authenticated
  WITH CHECK (employee_id = auth.uid());

CREATE POLICY "Admins can view all requests"
  ON support_requests
  FOR ALL
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM employees e
      WHERE e.id = auth.uid()
      AND e.is_admin = true
    )
  );
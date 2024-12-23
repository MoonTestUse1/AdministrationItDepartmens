/*
  # Create support requests table
  
  1. New Table
    - support_requests
      - id (uuid, primary key)
      - employee_id (uuid, foreign key to employees)
      - department (text)
      - request_type (request_type enum)
      - priority (request_priority enum)
      - status (request_status enum)
      - description (text)
      - created_at (timestamptz)
  
  2. Security
    - Enable RLS
    - Add request viewing, creation, and update policies
    - Add performance index for employee lookups
*/

-- Create support requests table
CREATE TABLE IF NOT EXISTS support_requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  employee_id uuid REFERENCES employees(id),
  department text NOT NULL,
  request_type request_type NOT NULL,
  priority request_priority NOT NULL,
  description text,
  status request_status NOT NULL DEFAULT 'new',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Enable RLS for support requests
ALTER TABLE support_requests ENABLE ROW LEVEL SECURITY;

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_support_requests_employee_id 
ON support_requests(employee_id);

-- Create RLS policies for support requests
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

CREATE POLICY "Employees can update their own requests"
  ON support_requests
  FOR UPDATE
  TO authenticated
  USING (employee_id = auth.uid());
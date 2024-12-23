/*
  # Create status history table

  1. New Tables
    - `status_history`
      - `id` (uuid, primary key)
      - `request_id` (uuid, foreign key to support_requests.id)
      - `old_status` (request_status)
      - `new_status` (request_status)
      - `changed_by` (uuid, foreign key to employees.id)
      - `changed_at` (timestamptz)

  2. Security
    - Enable RLS
    - Add policies for status history access
*/

CREATE TABLE IF NOT EXISTS status_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id uuid REFERENCES support_requests(id) ON DELETE CASCADE NOT NULL,
  old_status request_status,
  new_status request_status NOT NULL,
  changed_by uuid REFERENCES employees(id) ON DELETE CASCADE NOT NULL,
  changed_at timestamptz NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE status_history ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view status history of their requests"
  ON status_history
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM support_requests sr
      WHERE sr.id = status_history.request_id
      AND sr.employee_id = auth.uid()
    )
  );

CREATE POLICY "Admins can view all status history"
  ON status_history
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM employees e
      WHERE e.id = auth.uid()
      AND e.is_admin = true
    )
  );
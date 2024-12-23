/*
  # Update support requests policies

  1. Changes
    - Add RLS policies for support requests table
    - Allow authenticated users to create and view their requests
    - Allow admins to manage all requests

  2. Security
    - Enable RLS on support_requests table
    - Add policies for authenticated users
    - Add admin policies
*/

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can create their own requests" ON support_requests;
DROP POLICY IF EXISTS "Users can view their own requests" ON support_requests;
DROP POLICY IF EXISTS "Users can update their own requests" ON support_requests;
DROP POLICY IF EXISTS "Admins can view all requests" ON support_requests;

-- Create new policies
CREATE POLICY "Users can create requests"
  ON support_requests
  FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Users can view their own requests"
  ON support_requests
  FOR SELECT
  TO authenticated
  USING (
    auth.uid() = user_id OR
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid() AND department = 'it'
    )
  );

CREATE POLICY "Users can update their own requests"
  ON support_requests
  FOR UPDATE
  TO authenticated
  USING (
    auth.uid() = user_id OR
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid() AND department = 'it'
    )
  )
  WITH CHECK (
    auth.uid() = user_id OR
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid() AND department = 'it'
    )
  );

CREATE POLICY "IT department can manage all requests"
  ON support_requests
  FOR ALL
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid() AND department = 'it'
    )
  );
/*
  # Support Requests Table

  1. New Table
    - `support_requests`
      - `id` (uuid, primary key) - Unique identifier
      - `user_id` (text) - ID of the user who created the request
      - `department` (text) - Department the request is from
      - `request_type` (text) - Type of request (hardware/software/etc)
      - `priority` (text) - Request priority level
      - `description` (text) - Detailed description of the request
      - `status` (text) - Current status of the request
      - `created_at` (timestamp) - When the request was created

  2. Security
    - Enable RLS
    - Add policies for users and admins
*/

-- Create support requests table
CREATE TABLE IF NOT EXISTS support_requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id text NOT NULL,
  department text NOT NULL,
  request_type text NOT NULL CHECK (request_type IN ('hardware', 'software', 'network', 'access', 'other')),
  priority text NOT NULL CHECK (priority IN ('low', 'medium', 'high', 'critical')),
  description text,
  status text DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'resolved', 'closed')),
  created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE support_requests ENABLE ROW LEVEL SECURITY;

-- Create policies
DO $$ 
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE schemaname = 'public' 
    AND tablename = 'support_requests'
  ) THEN
    DROP POLICY IF EXISTS "Users can create their own requests" ON support_requests;
    DROP POLICY IF EXISTS "Users can view their own requests" ON support_requests;
    DROP POLICY IF EXISTS "Admins can update requests" ON support_requests;
  END IF;
END $$;

CREATE POLICY "Users can create their own requests"
  ON support_requests
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can view their own requests"
  ON support_requests
  FOR SELECT
  TO authenticated
  USING (auth.uid()::text = user_id OR auth.role() = 'admin');

CREATE POLICY "Admins can update requests"
  ON support_requests
  FOR UPDATE
  TO authenticated
  USING (auth.role() = 'admin')
  WITH CHECK (auth.role() = 'admin');
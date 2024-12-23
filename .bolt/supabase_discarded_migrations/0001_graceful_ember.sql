/*
  # Create support requests table

  1. New Tables
    - `support_requests`
      - `id` (uuid, primary key)
      - `user_id` (text)
      - `department` (text)
      - `request_type` (text) - for storing request type
      - `priority` (text)
      - `description` (text)
      - `status` (text)
      - `created_at` (timestamptz)

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
/*
  # Initial schema setup
  
  1. New Tables
    - `users`
      - `id` (uuid, primary key)
      - `first_name` (text)
      - `last_name` (text) 
      - `department` (text)
      - `password` (text)
      - `created_at` (timestamp)
    
    - `requests`
      - `id` (uuid, primary key)
      - `user_id` (uuid, foreign key)
      - `first_name` (text)
      - `last_name` (text)
      - `department` (text)
      - `urgency` (text)
      - `description` (text)
      - `status` (text)
      - `created_at` (timestamp)

  2. Security
    - Enable RLS on both tables
    - Add policies for authenticated users
*/

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  first_name text NOT NULL,
  last_name text NOT NULL,
  department text NOT NULL,
  password text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create requests table
CREATE TABLE IF NOT EXISTS requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id),
  first_name text NOT NULL,
  last_name text NOT NULL,
  department text NOT NULL,
  urgency text NOT NULL,
  description text,
  status text NOT NULL DEFAULT 'new',
  created_at timestamptz DEFAULT now(),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE requests ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can read own data"
  ON users
  FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can read all requests"
  ON requests
  FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can create requests"
  ON requests
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own requests"
  ON requests
  FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id);
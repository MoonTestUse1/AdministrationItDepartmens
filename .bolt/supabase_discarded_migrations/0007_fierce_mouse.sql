/*
  # Support Request System Tables

  1. New Tables
    - `support_requests`
      - `id` (uuid, primary key)
      - `employee_id` (uuid, references employees)
      - `department` (text)
      - `request_type` (enum)
      - `priority` (enum)
      - `status` (enum)
      - `description` (text)
      - `created_at` (timestamptz)
      - `last_status_change` (timestamptz)

    - `status_history`
      - `id` (uuid, primary key)
      - `request_id` (uuid, references support_requests)
      - `old_status` (enum)
      - `new_status` (enum)
      - `changed_by` (uuid, references employees)
      - `changed_at` (timestamptz)

  2. Security
    - Enable RLS on all tables
    - Add policies for employees and admins
*/

-- Create enum types
DO $$ BEGIN
    CREATE TYPE request_type AS ENUM ('hardware', 'software', 'network', 'access', 'other');
    CREATE TYPE request_priority AS ENUM ('low', 'medium', 'high', 'critical');
    CREATE TYPE request_status AS ENUM ('new', 'in_progress', 'resolved', 'closed');
EXCEPTION 
    WHEN duplicate_object THEN null;
END $$;

-- Create support requests table
CREATE TABLE IF NOT EXISTS support_requests (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id uuid REFERENCES employees(id) NOT NULL,
    department text NOT NULL,
    request_type request_type NOT NULL,
    priority request_priority NOT NULL,
    status request_status NOT NULL DEFAULT 'new',
    description text,
    created_at timestamptz NOT NULL DEFAULT now(),
    last_status_change timestamptz DEFAULT now()
);

-- Create status history table
CREATE TABLE IF NOT EXISTS status_history (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id uuid REFERENCES support_requests(id) ON DELETE CASCADE,
    old_status request_status,
    new_status request_status NOT NULL,
    changed_by uuid REFERENCES employees(id) NOT NULL,
    changed_at timestamptz NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE support_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE status_history ENABLE ROW LEVEL SECURITY;

-- Create policies for support_requests
DO $$ BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_policies 
        WHERE tablename = 'support_requests' 
        AND policyname = 'Employees can view their own requests'
    ) THEN
        CREATE POLICY "Employees can view their own requests"
            ON support_requests
            FOR SELECT
            TO authenticated
            USING (employee_id = auth.uid());
    END IF;

    IF NOT EXISTS (
        SELECT FROM pg_policies 
        WHERE tablename = 'support_requests' 
        AND policyname = 'Employees can create their own requests'
    ) THEN
        CREATE POLICY "Employees can create their own requests"
            ON support_requests
            FOR INSERT
            TO authenticated
            WITH CHECK (employee_id = auth.uid());
    END IF;

    IF NOT EXISTS (
        SELECT FROM pg_policies 
        WHERE tablename = 'support_requests' 
        AND policyname = 'Admins can view all requests'
    ) THEN
        CREATE POLICY "Admins can view all requests"
            ON support_requests
            FOR ALL
            TO authenticated
            USING (auth.jwt() ->> 'role' = 'admin');
    END IF;
END $$;

-- Create policies for status_history
DO $$ BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_policies 
        WHERE tablename = 'status_history' 
        AND policyname = 'Employees can view status history of their requests'
    ) THEN
        CREATE POLICY "Employees can view status history of their requests"
            ON status_history
            FOR SELECT
            TO authenticated
            USING (
                EXISTS (
                    SELECT 1 FROM support_requests
                    WHERE id = status_history.request_id
                    AND employee_id = auth.uid()
                )
            );
    END IF;

    IF NOT EXISTS (
        SELECT FROM pg_policies 
        WHERE tablename = 'status_history' 
        AND policyname = 'Admins can view all status history'
    ) THEN
        CREATE POLICY "Admins can view all status history"
            ON status_history
            FOR ALL
            TO authenticated
            USING (auth.jwt() ->> 'role' = 'admin');
    END IF;
END $$;

-- Create status update trigger
CREATE OR REPLACE FUNCTION update_request_status_history()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE' AND OLD.status IS DISTINCT FROM NEW.status) THEN
        INSERT INTO status_history (
            request_id,
            old_status,
            new_status,
            changed_by
        ) VALUES (
            NEW.id,
            OLD.status,
            NEW.status,
            auth.uid()
        );
        
        NEW.last_status_change = now();
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger
DROP TRIGGER IF EXISTS track_request_status_changes ON support_requests;
CREATE TRIGGER track_request_status_changes
    BEFORE UPDATE ON support_requests
    FOR EACH ROW
    EXECUTE FUNCTION update_request_status_history();
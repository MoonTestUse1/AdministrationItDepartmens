-- Create the postgres superuser
CREATE USER postgres WITH PASSWORD 'postgres' SUPERUSER;

-- Create the database
CREATE DATABASE support_db;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE support_db TO postgres; 
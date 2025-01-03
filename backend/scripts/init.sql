CREATE TYPE requeststatus AS ENUM ('new', 'in_progress', 'completed', 'rejected');
CREATE TYPE requestpriority AS ENUM ('low', 'medium', 'high');

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    department VARCHAR NOT NULL,
    office VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL
);

CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    status requeststatus NOT NULL,
    priority requestpriority NOT NULL,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    access_token VARCHAR NOT NULL UNIQUE,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX ix_employees_id ON employees(id);
CREATE INDEX ix_employees_last_name ON employees(last_name);
CREATE INDEX ix_requests_id ON requests(id);
CREATE INDEX ix_tokens_id ON tokens(id);
CREATE INDEX ix_tokens_access_token ON tokens(access_token); 
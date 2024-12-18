-- Create the user role if it does not exist
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'user') THEN
      CREATE ROLE "user" WITH LOGIN PASSWORD 'password';
   END IF;
END
$$;

-- Create the database if it does not exist
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mydb') THEN
      CREATE DATABASE mydb;
   END IF;
END
$$;

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE mydb TO "user";

-- Connect to the mydb database
\c mydb;

-- Create the test table if it does not exist
CREATE TABLE IF NOT EXISTS test_table (
   id SERIAL PRIMARY KEY,
   data TEXT
);

-- Insert sample data into the table if it's not already present
INSERT INTO test_table (data)
SELECT 'Hello from the database!'
WHERE NOT EXISTS (SELECT 1 FROM test_table WHERE data = 'Hello from the database!');

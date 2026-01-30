-- Example Demo Data SQL File
-- 
-- This is a template SQL file for loading demo data.
-- Use {PREFIX} placeholder for table prefixes that will be replaced at runtime.
--
-- Example:
--   CREATE TABLE {PREFIX}example (id INT PRIMARY KEY);
--   INSERT INTO {PREFIX}example VALUES (1);

-- Example tables without prefix (generic)
CREATE TABLE IF NOT EXISTS demo_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS demo_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO demo_users (username, email) VALUES
('admin', 'admin@example.com'),
('user1', 'user1@example.com'),
('user2', 'user2@example.com');

INSERT INTO demo_products (name, description, price) VALUES
('Product A', 'This is product A', 19.99),
('Product B', 'This is product B', 29.99),
('Product C', 'This is product C', 39.99);

-- Example with table prefix placeholder
-- CREATE TABLE IF NOT EXISTS {PREFIX}custom_table (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     data VARCHAR(255)
-- );
-- 
-- INSERT INTO {PREFIX}custom_table (data) VALUES ('Example data');

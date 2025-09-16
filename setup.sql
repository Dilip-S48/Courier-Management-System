-- Create the database for the courier management system
CREATE DATABASE IF NOT EXISTS courier_db;

-- Use the newly created database
USE courier_db;

-- Create the users table to store information about administrators, employees, and clients
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'employee', 'client') NOT NULL,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(20),
    address TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the couriers table to store details of each parcel
CREATE TABLE IF NOT EXISTS couriers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_number VARCHAR(255) NOT NULL UNIQUE,
    sender_name VARCHAR(255) NOT NULL,
    sender_address TEXT NOT NULL,
    receiver_name VARCHAR(255) NOT NULL,
    receiver_address TEXT NOT NULL,
    parcel_description TEXT,
    status ENUM('Pending', 'In Transit', 'Delivered', 'Cancelled') NOT NULL DEFAULT 'Pending',
    assigned_employee_id INT,
    client_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_employee_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (client_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create a tracking history table to log status updates for each courier
CREATE TABLE IF NOT EXISTS tracking_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    courier_id INT NOT NULL,
    status ENUM('Pending', 'In Transit', 'Delivered', 'Cancelled') NOT NULL,
    location VARCHAR(255),
    remarks TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (courier_id) REFERENCES couriers(id) ON DELETE CASCADE
);

-- Insert a default admin user for initial login
-- You can change the username and password as needed
INSERT INTO users (username, password, role, full_name, email)
VALUES ('admin', 'admin123', 'admin', 'Administrator', 'admin@courier.com')
ON DUPLICATE KEY UPDATE password='admin123';

-- Insert a default employee user for testing
INSERT INTO users (username, password, role, full_name, email)
VALUES ('employee1', 'emp123', 'employee', 'John Doe', 'john.doe@courier.com')
ON DUPLICATE KEY UPDATE password='emp123';

-- Insert a default client user for testing
INSERT INTO users (username, password, role, full_name, email)
VALUES ('client1', 'client123', 'client', 'Jane Smith', 'jane.smith@example.com')
ON DUPLICATE KEY UPDATE password='client123';
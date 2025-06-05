-- Create database and user
CREATE DATABASE IF NOT EXISTS my_db;
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON my_db.* TO 'user'@'%';

-- Switch to the new DB
USE my_db;

-- Create table
CREATE TABLE IF NOT EXISTS North_user_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(100),
    login_location VARCHAR(100),
    login_time DATETIME,
    topic VARCHAR(100)
);
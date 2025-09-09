-- Create the `todozen` database if it does not exist
CREATE DATABASE IF NOT EXISTS todozen;

-- Use the `todozen` database
USE todozen;

-- Create the `users` table
CREATE TABLE IF NOT EXISTS users (
    UserID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each user
    RewardPoints INT DEFAULT 0,            -- Reward points for the user
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- User creation timestamp
    UNIQUE(UserID) -- Ensures that the UserID is unique for each user
);

-- Create the `tasks` table without the UserID column
CREATE TABLE IF NOT EXISTS tasks (
    TaskID INT AUTO_INCREMENT PRIMARY KEY,    -- Unique ID for each task
    Title VARCHAR(255) NOT NULL,               -- Title of the task
    Priority ENUM('High', 'Medium', 'Low') NOT NULL, -- Priority level of the task
    Completed BOOLEAN DEFAULT FALSE,           -- Completion status of the task
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Task creation timestamp
    Deadline DATE NOT NULL,                    -- Deadline for the task
    RewardPoints INT DEFAULT 10                -- Reward points for completing the task
);

-- Insert a few sample users into the users table
INSERT INTO users (RewardPoints) VALUES (0);  -- User 1 with 0 points
INSERT INTO users (RewardPoints) VALUES (10); -- User 2 with 10 points
INSERT INTO users (RewardPoints) VALUES (20); -- User 3 with 20 points

-- Query to verify the inserted users
SELECT * FROM users;

-- Insert a sample task into the tasks table
INSERT INTO tasks (Title, Priority, Completed, CreatedAt, Deadline, RewardPoints)
VALUES ('Complete MySQL Tutorial', 'High', FALSE, NOW(), '2025-01-10', 10);

-- Query to verify the inserted task
SELECT * FROM tasks;

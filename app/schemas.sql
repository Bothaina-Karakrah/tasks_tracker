--Drop tables if exists
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Create category table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL
);

-- Create task table
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES category(id) ON DELETE SET NULL,

    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    priority INTEGER NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'todo',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    completed_at TIMESTAMP,
    time_spent_minutes INTEGER DEFAULT 0
);

-- Performance indexes
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_category_id ON task(category_id);
CREATE INDEX idx_task_status ON task(status);
CREATE INDEX idx_task_due_date ON task(due_date);
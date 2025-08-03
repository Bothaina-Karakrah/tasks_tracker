-- Drop tasks table if it exists
DROP TABLE IF EXISTS tasks;

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,

    title VARCHAR(100) NOT NULL,
    description TEXT,

    priority VARCHAR(10) NOT NULL DEFAULT 'medium', -- ENUM: 'low', 'medium', 'high'
    status VARCHAR(20) NOT NULL DEFAULT 'todo',     -- ENUM: 'todo', 'in_progress', 'completed'

    category VARCHAR(100) NOT NULL DEFAULT 'General',

    estimated_hours INTEGER NOT NULL DEFAULT 1,
    actual_hours INTEGER DEFAULT 0,

    started_at TIMESTAMP,
    due_date TIMESTAMP,
    completed_at TIMESTAMP,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_category ON tasks(category);
# Task Management System - Setup Guide

## Project Structure
```
task-management-system/
├── main.py                 # FastAPI backend
├── index.html             # Frontend interface
├── requirements.txt       # Python dependencies
├── tasks.db              # SQLite database (auto-created)
└── README.md             # This file
```

## Requirements (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
```

## Installation & Setup

### 1. Create Virtual Environment
```bash
# Create virtual environment
python -m venv task_env

# Activate virtual environment
# On Windows:
task_env\Scripts\activate
# On macOS/Linux:
source task_env/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
# Start the FastAPI server
python main.py

# The server will start on http://localhost:8000
```

### 4. Access the Application
- Open your web browser
- Navigate to the `index.html` file directly, or
- Serve it through a simple HTTP server:
```bash
# Using Python's built-in server
python -m http.server 3000

# Then open http://localhost:3000 in your browser
```

## API Endpoints

### Tasks
- `GET /tasks/` - Get all tasks (with optional filters)
- `POST /tasks/` - Create a new task
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

### Analytics
- `GET /analytics/` - Get productivity analytics
- `GET /categories/` - Get all task categories

### Query Parameters for GET /tasks/
- `status`: Filter by status (todo, in_progress, completed)
- `priority`: Filter by priority (low, medium, high)
- `category`: Filter by category name

## Features Implemented

### ✅ Task Management
- Create, read, update, delete tasks
- Task priorities (Low, Medium, High)
- Task statuses (To Do, In Progress, Completed)
- Task categories
- Time tracking (estimated vs actual hours)
- Task descriptions

### ✅ Filtering & Search
- Filter by status, priority, and category
- Real-time filtering
- Dynamic category loading

### ✅ Analytics Dashboard
- Total tasks overview
- Completion rate calculation
- Average completion time
- Tasks breakdown by category
- Tasks breakdown by priority
- Daily completion trends (last 7 days)

### ✅ User Interface
- Modern, responsive design
- Tabbed interface (Tasks, Create, Analytics)
- Modal dialogs for editing
- Real-time updates
- Success/error messaging
- Mobile-friendly layout

### ✅ Database
- SQLite database with SQLAlchemy ORM
- Automatic table creation
- Data persistence
- Proper relationships and constraints

## API Testing

You can test the API using curl or any API testing tool:

```bash
# Create a new task
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Study FastAPI documentation",
    "priority": "high",
    "category": "Learning",
    "estimated_hours": 4
  }'

# Get all tasks
curl "http://localhost:8000/tasks/"

# Get analytics
curl "http://localhost:8000/analytics/"
```

## Advanced Features You Can Add

### 1. Authentication & User Management
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt

# Add user authentication
# Multiple users with separate task lists
```

### 2. Task Dependencies
```python
# Add task relationships
class TaskDependency(Base):
    __tablename__ = "task_dependencies"
    
    id = Column(Integer, primary_key=True)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"))
    child_task_id = Column(Integer, ForeignKey("tasks.id"))
```

### 3. File Attachments
```python
from fastapi import UploadFile, File

@app.post("/tasks/{task_id}/attachments/")
async def upload_attachment(task_id: int, file: UploadFile = File(...)):
    # Handle file uploads
    pass
```

### 4. Real-time Updates with WebSocket
```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Real-time task updates
    pass
```

### 5. Export Functionality
```python
import pandas as pd
from fastapi.responses import StreamingResponse

@app.get("/export/tasks/")
def export_tasks():
    # Export tasks to CSV/Excel
    pass
```

### 6. Advanced Analytics
- Productivity trends over time
- Time estimation accuracy
- Task completion patterns
- Category performance metrics
- Burndown charts

## Database Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR DEFAULT 'todo',
    priority VARCHAR DEFAULT 'medium',
    category VARCHAR,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    estimated_hours INTEGER DEFAULT 1,
    actual_hours INTEGER
);
```

## Testing

### Unit Tests Example
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "priority": "high"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Deployment Options

### 1. Local Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Production with Gunicorn
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 3. Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Cloud Deployment
- **Heroku**: Add `Procfile` with `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Railway**: Direct deployment from GitHub
- **AWS EC2**: Using Docker or direct installation
- **Google Cloud Run**: Container deployment

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the frontend is served from the same domain or CORS is properly configured
2. **Database Not Found**: The SQLite database is created automatically on first run
3. **Port Already in Use**: Change the port in `uvicorn.run()` or kill the existing process
4. **Import Errors**: Ensure all dependencies are installed in the virtual environment

### Development Tips

1. **Auto-reload**: Use `--reload` flag during development
2. **API Documentation**: Visit `http://localhost:8000/docs` for interactive API docs
3. **Database Inspection**: Use SQLite browser tools to inspect the database
4. **Logging**: Add logging for debugging: `import logging; logging.basicConfig(level=logging.INFO)`

This project demonstrates a complete full-stack application with modern web technologies, proper database design, and professional development practices!
from typing import Optional, List, Dict
from pydantic import BaseModel, constr
from datetime import datetime
from app.models import TaskStatus, TaskPriority

# ========== Task Model ==========
class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    category: Optional[str] = "General"
    estimated_days: int = 1

    status: TaskStatus = TaskStatus.TODO
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    actual_days: Optional[int] = 0

class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=100)] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    actual_days: Optional[int] = None
    category: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# ========== Analytics Model ==========
class AnalyticsResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    completion_rate: float
    avg_completion_time: float
    tasks_by_category: Dict[str, int]
    tasks_by_priority: Dict[str, int]
    daily_completions: List[Dict[str, int]]
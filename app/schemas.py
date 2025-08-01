# app/schemas.py
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime
from enum import Enum

# ========== User ==========
class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# ========== Category ==========
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# ========== Task ==========
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    priority: int
    status: TaskStatus = TaskStatus.pending
    started_at: datetime
    due_date: datetime
    completed_at: Optional[datetime] = None
    time_spent_minutes: Optional[int] = 0
    category: Optional[str] = None

    @validator('due_date')
    def check_due_date(cls, v):
        if v and v < datetime.utcnow():
            raise ValueError("due_date cannot be in the past")
        return v

class TaskCreate(TaskBase):
    user_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    time_spent_minutes: Optional[int] = None
    category: Optional[str] = None

class Task(TaskBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Dict, Any
from app.database import get_db
from app.models import Task

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def get_analytics(db: Session = Depends(get_db)):
    """Get task analytics and statistics"""

    # Basic counts
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()
    in_progress_tasks = db.query(Task).filter(Task.status == "in_progress").count()

    # Completion rate
    completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)

    # Average completion time (for completed tasks with actual_hours)
    avg_completion_query = db.query(func.avg(Task.actual_hours)).filter(
        and_(Task.status == "completed", Task.actual_hours.isnot(None))
    ).scalar()
    avg_completion_time = round(avg_completion_query, 1) if avg_completion_query else 0

    # Tasks by category
    tasks_by_category = {}
    category_counts = db.query(Task.category, func.count(Task.id)).group_by(Task.category).all()
    for category, count in category_counts:
        tasks_by_category[category or "General"] = count

    # Tasks by priority
    tasks_by_priority = {}
    priority_counts = db.query(Task.priority, func.count(Task.id)).group_by(Task.priority).all()
    for priority, count in priority_counts:
        tasks_by_priority[priority] = count

    # Daily completions for the last 7 days
    daily_completions = {}
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)  # Last 7 days including today

    for i in range(7):
        current_date = start_date + timedelta(days=i)
        completed_count = db.query(Task).filter(
            and_(
                Task.status == "completed",
                func.date(Task.completed_at) == current_date
            )
        ).count()
        daily_completions[current_date.isoformat()] = {"completed": completed_count}

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completion_rate": completion_rate,
        "avg_completion_time": avg_completion_time,
        "tasks_by_category": tasks_by_category,
        "tasks_by_priority": tasks_by_priority,
        "daily_completions": daily_completions
    }
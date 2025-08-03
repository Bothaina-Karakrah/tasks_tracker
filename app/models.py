from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from enum import Enum
from sqlalchemy import Enum as SqlEnum

# ========== Enums ==========
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# ========== Task Model ==========
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    priority: Mapped[TaskPriority] = mapped_column(
        SqlEnum(TaskPriority, name="task_priority"), default=TaskPriority.MEDIUM, nullable=False
    )
    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus, name="task_status"), default=TaskStatus.TODO, nullable=False
    )

    category: Mapped[str] = mapped_column(String(100), default="General", nullable=False, index=True)

    estimated_days: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    actual_days: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)
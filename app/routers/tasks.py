"""
Task Endpoints
- POST   /tasks           → Create a new task
- GET    /tasks           → Retrieve all tasks
- GET    /tasks/{task_id} → Retrieve a specific task
- PATCH  /tasks/{task_id} → Partially update a task
- PUT    /tasks/{task_id} → Fully update a task
- DELETE /tasks/{task_id} → Delete a task
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models, schemas
from app.database import async_session

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Dependency: Get async DB session
async def get_db():
    async with async_session() as session:
        yield session


@router.post("/", response_model=schemas.Task)
async def create_task(task_data: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(models.User).where(models.User.id == task_data.user_task_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create and save task
    new_task = models.Task(**task_data.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/", response_model=List[schemas.Task])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Task))
    return result.scalars().all()


@router.get("/{task_id}", response_model=schemas.Task)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, updated_data: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.put("/{task_id}", response_model=schemas.Task)
async def update_full_task(task_id: int, updated_data: schemas.TaskBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in updated_data.model_dump().items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return Response(status_code=204)
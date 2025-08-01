"""
User Endpoints
- POST   /users           → Create a new user
- GET    /users           → Retrieve all users
- GET    /users/{user_id}      → Retrieve a specific user
- PATCH  /users/{user_id}      → Partially update a user
- DELETE /users/{user_id}      → Delete a specific user
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import async_session
from app import models, schemas
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])


# Dependency: Get async DB session
async def get_db():
    async with async_session() as session:
        yield session


@router.post("/", response_model=schemas.User)
async def create_user(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(models.User).where(models.User.email == user_data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    new_user = models.User(**user_data.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[schemas.User])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    return result.scalars().all()


@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user_update: schemas.UserBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return Response(status_code=204)
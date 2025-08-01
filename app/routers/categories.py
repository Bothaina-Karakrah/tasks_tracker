from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models, schemas
from app.database import async_session

router = APIRouter(prefix="/categories", tags=["Categories"])

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=schemas.Category)
async def create_category(category_data: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    existing_category = await db.execute(select(models.Category).where(models.Category.name == category_data.name))
    if existing_category.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    new_category = models.Category(**category_data.model_dump())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

@router.get("/", response_model=List[schemas.Category])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Category))
    return result.scalars().all()

@router.get("/{category_id}", response_model=schemas.Category)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.scalar(select(models.Category).where(models.Category.id == category_id))
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.patch("/{category_id}", response_model=schemas.Category)
async def update_category(category_id: int, category_data: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    category = await db.scalar(select(models.Category).where(models.Category.id == category_id))
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category_data.model_dump().items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.scalar(select(models.Category).where(models.Category.id == category_id))
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(category)
    await db.commit()
    return Response(status_code=204)
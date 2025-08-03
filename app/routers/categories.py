from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from typing import List
from app.database import get_db
from app.models import Task

router = APIRouter()


@router.get("/", response_model=List[str])
async def get_categories(db: Session = Depends(get_db)):
    """Get all unique categories from tasks"""
    categories = db.query(distinct(Task.category)).filter(Task.category.isnot(None)).all()
    # Extract the category names from the query result tuples
    category_list = [category[0] for category in categories if category[0]]

    # Add default category if no categories exist
    if not category_list:
        category_list = ["General"]

    return sorted(category_list)
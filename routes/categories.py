from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from database import get_database
from models import Category
router = APIRouter()

# Predefined category map
default_categories = {
    'health': 'Все о нашем здоровье',
    'understand': 'Как понять себя',
    'security': 'Моя безопасность',
    'relationship': 'Отношения',
    'education': 'Просвещение',
}


# Endpoint to initialize categories in the database (one-time use)
@router.post("/categories/init")
async def initialize_categories():
    db = get_database()
    for key, value in default_categories.items():
        existing_category = await db.categories.find_one({"key": key})
        if not existing_category:
            await db.categories.insert_one({"key": key, "value": value})
    return {"message": "Categories initialized."}


# Endpoint to add a new category
@router.post("/categories/")
async def add_category(category: Category):
    db = get_database()
    existing_category = await db.categories.find_one({"key": category.key})
    if existing_category:
        raise HTTPException(
            status_code=400, detail=f"Category with key '{category.key}' already exists."
        )
    await db.categories.insert_one(category.dict())
    return {"message": "Category added successfully.", "category": category}


# Endpoint to get all categories
@router.get("/categories/")
async def get_all_categories():
    db = get_database()
    categories = await db.categories.find().to_list(length=None)
    return [{"key": category["key"], "value": category["value"]} for category in categories]

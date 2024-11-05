# routes/affirmations.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
from typing import List
from database import get_database  # Assuming you have a database helper function

router = APIRouter()

class AffirmationRequest(BaseModel):
    affirmations: List[constr(strip_whitespace=True, min_length=1)]  # List of exactly 7 affirmations

@router.post("/affirmations/")
async def save_affirmations(data: AffirmationRequest):
    if len(data.affirmations) != 7:
        raise HTTPException(status_code=400, detail="The list must contain exactly 7 affirmations.")
    
    db = get_database()
    await db.affirmations.delete_many({})  # Clear existing affirmations
    await db.affirmations.insert_one({"affirmations": data.affirmations})
    return {"message": "Affirmations saved successfully"}

@router.get("/affirmations/{day}")
async def get_affirmation(day: int):
    if day < 1 or day > 7:
        raise HTTPException(status_code=400, detail="Day must be between 1 and 7")

    db = get_database()
    doc = await db.affirmations.find_one()
    if not doc or "affirmations" not in doc:
        raise HTTPException(status_code=404, detail="No affirmations found for this week.")
    
    affirmation = doc["affirmations"][day - 1]
    return {"day": day, "affirmation": affirmation}

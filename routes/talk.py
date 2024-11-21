from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from bson import ObjectId
from datetime import datetime
from database import get_database
from models import Talk, Answer


router = APIRouter()


# Endpoint to create a talk
@router.post("/talks/")
async def create_talk(talk: Talk):
    db = get_database()
    talk_data = talk.dict()
    talk_data["created_at"] = datetime.utcnow()
    new_talk = await db.talks.insert_one(talk_data)
    created_talk = await db.talks.find_one({"_id": new_talk.inserted_id})
    if created_talk:
        created_talk["_id"] = str(created_talk["_id"])
        return created_talk
    raise HTTPException(status_code=500, detail="Talk could not be created")


# Endpoint to get all talks
@router.get("/talks/")
async def get_all_talks():
    db = get_database()
    talks = await db.talks.find().to_list(length=None)
    for talk in talks:
        talk["_id"] = str(talk["_id"])
    return talks


# Endpoint to get a talk by ID
@router.get("/talks/{talk_id}")
async def get_talk_by_id(talk_id: str):
    db = get_database()
    talk = await db.talks.find_one({"_id": ObjectId(talk_id)})
    if talk:
        talk["_id"] = str(talk["_id"])
        return talk
    raise HTTPException(status_code=404, detail="Talk not found")


# Endpoint to add an answer to a talk
@router.put("/talks/{talk_id}/add_answer")
async def add_answer_to_talk(talk_id: str, answer: Answer):
    db = get_database()
    new_answer = answer.dict()
    new_answer["created_at"] = datetime.utcnow()
    update_result = await db.talks.update_one(
        {"_id": ObjectId(talk_id)},
        {"$push": {"answers": new_answer}}
    )
    if update_result.modified_count == 1:
        updated_talk = await db.talks.find_one({"_id": ObjectId(talk_id)})
        if updated_talk:
            updated_talk["_id"] = str(updated_talk["_id"])
            return updated_talk
    raise HTTPException(status_code=404, detail="Talk not found or answer could not be added")


# Endpoint to update the question of a talk
@router.put("/talks/{talk_id}/update_question")
async def update_talk_question(talk_id: str, new_question: str):
    db = get_database()
    update_result = await db.talks.update_one(
        {"_id": ObjectId(talk_id)},
        {"$set": {"question": new_question}}
    )
    if update_result.modified_count == 1:
        updated_talk = await db.talks.find_one({"_id": ObjectId(talk_id)})
        if updated_talk:
            updated_talk["_id"] = str(updated_talk["_id"])
            return updated_talk
    raise HTTPException(status_code=404, detail="Talk not found or question could not be updated")

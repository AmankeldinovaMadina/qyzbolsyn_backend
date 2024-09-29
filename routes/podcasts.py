from fastapi import APIRouter, HTTPException
from models import Podcast
from database import get_database
from bson import ObjectId

router = APIRouter()

@router.post("/podcasts/")
async def create_podcast(podcast: Podcast):
    db = get_database()
    podcast_data = podcast.dict()
    new_podcast = await db.podcasts.insert_one(podcast_data)
    created_podcast = await db.podcasts.find_one({"_id": new_podcast.inserted_id})
    if created_podcast:
        created_podcast["_id"] = str(created_podcast["_id"])
        return created_podcast
    raise HTTPException(status_code=500, detail="Podcast could not be created")

@router.get("/podcasts/")
async def get_all_podcasts():
    db = get_database()
    podcasts = await db.podcasts.find().to_list(length=None)
    for podcast in podcasts:
        podcast["_id"] = str(podcast["_id"])
    return podcasts

@router.get("/podcasts/{podcast_id}")
async def get_podcast_by_id(podcast_id: str):
    db = get_database()
    podcast = await db.podcasts.find_one({"_id": ObjectId(podcast_id)})
    if podcast:
        podcast["_id"] = str(podcast["_id"])
        return podcast
    raise HTTPException(status_code=404, detail="Podcast not found")

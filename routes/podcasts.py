from fastapi import APIRouter, HTTPException
from models import Podcast
from database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# Endpoint to create a podcast
@router.post("/podcasts/")
async def create_podcast(podcast: Podcast):
    db = get_database()
    podcast_data = podcast.dict()
    podcast_data["created_at"] = datetime.utcnow()  # Add the current time
    new_podcast = await db.podcasts.insert_one(podcast_data)
    created_podcast = await db.podcasts.find_one({"_id": new_podcast.inserted_id})
    if created_podcast:
        created_podcast["_id"] = str(created_podcast["_id"])
        return created_podcast
    raise HTTPException(status_code=500, detail="Podcast could not be created")

# Endpoint to get all podcasts
@router.get("/podcasts/")
async def get_all_podcasts():
    db = get_database()
    podcasts = await db.podcasts.find().to_list(length=None)
    for podcast in podcasts:
        podcast["_id"] = str(podcast["_id"])
    return podcasts

# Endpoint to get a podcast by ID
@router.get("/podcasts/{podcast_id}")
async def get_podcast_by_id(podcast_id: str):
    db = get_database()
    podcast = await db.podcasts.find_one({"_id": ObjectId(podcast_id)})
    if podcast:
        podcast["_id"] = str(podcast["_id"])
        return podcast
    raise HTTPException(status_code=404, detail="Podcast not found")

# Endpoint to get the latest podcast
@router.get("/podcasts/latest")
async def get_latest_podcast():
    db = get_database()
    latest_podcast = await db.podcasts.find().sort("created_at", -1).limit(1).to_list(length=1)
    if latest_podcast:
        latest_podcast[0]["_id"] = str(latest_podcast[0]["_id"])
        return latest_podcast[0]
    raise HTTPException(status_code=404, detail="No podcasts found")

from fastapi import APIRouter, HTTPException
from models import Post
from database import get_database
from bson import ObjectId

router = APIRouter()

@router.post("/posts/")
async def create_post(post: Post):
    db = get_database()
    post_data = post.dict()
    new_post = await db.posts.insert_one(post_data)
    created_post = await db.posts.find_one({"_id": new_post.inserted_id})
    if created_post:
        created_post["_id"] = str(created_post["_id"])
        return created_post
    raise HTTPException(status_code=500, detail="Post could not be created")

@router.get("/posts/")
async def get_all_posts():
    db = get_database()
    posts = await db.posts.find().to_list(length=None)
    for post in posts:
        post["_id"] = str(post["_id"])
    return posts

@router.get("/posts/{post_id}")
async def get_post_by_id(post_id: str):
    db = get_database()
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if post:
        post["_id"] = str(post["_id"])
        return post
    raise HTTPException(status_code=404, detail="Post not found")

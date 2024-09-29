from fastapi import FastAPI
from database import connect_to_mongo
from routes.posts import router as posts_router
from routes.podcasts import router as podcasts_router

app = FastAPI()

# Connect to MongoDB
connect_to_mongo()

# Include the posts router
app.include_router(posts_router)
app.include_router(podcasts_router) 
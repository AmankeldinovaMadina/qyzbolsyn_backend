from fastapi import FastAPI
from database import connect_to_mongo
from routes.posts import router as posts_router
from routes.podcasts import router as podcasts_router
from routes.affirmation import router as affirmations_router


app = FastAPI()

# Connect to MongoDB
connect_to_mongo()


# app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(podcasts_router)

# Include the posts router
app.include_router(posts_router)
app.include_router(podcasts_router) 
app.include_router(affirmations_router)






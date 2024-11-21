from fastapi import FastAPI
from database import connect_to_mongo
from routes.posts import router as posts_router
from routes.podcasts import router as podcasts_router
from routes.affirmation import router as affirmations_router
from routes.talk import router as talks_router  # New import for talks router
from routes.categories import router as categories_router

app = FastAPI()

# Connect to MongoDB
connect_to_mongo()

# Include routers
app.include_router(posts_router, prefix="/posts", tags=["Posts"])
app.include_router(podcasts_router, prefix="/podcasts", tags=["Podcasts"])
app.include_router(affirmations_router, prefix="/affirmations", tags=["Affirmations"])
app.include_router(talks_router, prefix="/talks", tags=["Talks"])  # Include talks router
app.include_router(categories_router, prefix="/categories", tags=["Categories"])



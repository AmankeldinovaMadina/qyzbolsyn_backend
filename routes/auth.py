# from fastapi import APIRouter, Request, Depends, HTTPException
# from authlib.integrations.starlette_client import OAuth
# from starlette.config import Config
# from database import get_database  # Assuming MongoDB is being used
# from auth_utils import create_jwt_token
# from fastapi.security import OAuth2PasswordRequestForm
# from passlib.context import CryptContext

# router = APIRouter()

# # Load OAuth configuration from environment
# config = Config('.env')
# oauth = OAuth(config)

# oauth.register(
#     name='google',
#     client_id=config('GOOGLE_CLIENT_ID'),
#     client_secret=config('GOOGLE_CLIENT_SECRET'),
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     redirect_uri='http://localhost:8000/auth/callback',
#     client_kwargs={'scope': 'openid email profile'}
# )

# # Password hashing setup
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # MongoDB collection for users (assuming you're using MongoDB)
# db = get_database().users


# @router.post("/auth/register")
# async def register(email: str, password: str):
#     hashed_password = pwd_context.hash(password)
#     user = {"email": email, "password": hashed_password}
#     await db.insert_one(user)
#     return {"msg": "User registered successfully"}


# @router.post("/auth/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await db.find_one({"email": form_data.username})
#     if not user or not pwd_context.verify(form_data.password, user["password"]):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     token = create_jwt_token(user["email"])
#     return {"access_token": token, "token_type": "bearer"}


# @router.get("/auth/google")
# async def google_login(request: Request):
#     redirect_uri = 'http://localhost:8000/auth/google/callback'
#     return await oauth.google.authorize_redirect(request, redirect_uri)


# @router.get("/auth/google/callback")
# async def google_callback(request: Request):
#     token = await oauth.google.authorize_access_token(request)
#     user_info = await oauth.google.parse_id_token(request, token)
#     user = await db.find_one({"email": user_info["email"]})
#     if not user:
#         user = {"email": user_info["email"], "password": None}  # No password if Google login
#         await db.insert_one(user)
#     jwt_token = create_jwt_token(user_info["email"])
#     return {"access_token": jwt_token, "token_type": "bearer"}

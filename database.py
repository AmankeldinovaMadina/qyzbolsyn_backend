from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO")
client = AsyncIOMotorClient(MONGO_DB_URL, tls=True, tlsAllowInvalidCertificates=True)

def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGO_DB_URL)

def get_database():
    return client.qyzbolsyn  # Replace with your database name

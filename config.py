import os

import requests
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
load_dotenv()

client_id, client_secret, access_token = (
    os.getenv("CLIENT_ID"),
    os.getenv("CLIENT_SECRET"),
    os.getenv("ACCESS_TOKEN"),
)

ai_21_api_key = os.getenv("AI_21_API_KEY")

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.stepsisbot
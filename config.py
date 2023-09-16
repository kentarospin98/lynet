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

# url = "https://id.twitch.tv/oauth2/token"

# payload = f"client_id={os.getenv('CLIENT_ID')}&client_secret={os.getenv('CLIENT_SECRET')}&grant_type=client_credentials"
# headers = {"Content-Type": "application/x-www-form-urlencoded"}

# response = requests.request("POST", url, headers=headers, data=payload)
# if not response.ok:
#     raise RuntimeError("Failed to login")

# access_token = response.json()["access_token"]

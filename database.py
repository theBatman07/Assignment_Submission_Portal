from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
import os 

load_dotenv()

# Database settings
# Load the MONGODB_URL from .env
MONGO_DETAILS = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.assignment_portal
users_collection = database.get_collection("users")
assignments_collection = database.get_collection("assignments")

# Helper to format ObjectId in MongoDB documents
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"],
    }

def assignment_helper(assignment) -> dict:
    return {
        "id": str(assignment["_id"]),
        "userId": assignment["userId"],
        "task": assignment["task"],
        "admin": assignment["admin"],
        "status": assignment["status"],
        "timestamp": assignment["timestamp"],
    }

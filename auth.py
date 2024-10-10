from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from database import users_collection
from models import UserModel
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2 password bearer token setup; the token will be passed with the requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to verify user credentials during login
async def verify_user(username: str, password: str):
    user = await users_collection.find_one({"username": username})
    if user and pwd_context.verify(password, user["password"]):
        return user
    return False

# Function to get the current authenticated user based on the token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await users_collection.find_one({"_id": ObjectId(token)})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

from fastapi import APIRouter, HTTPException, Depends
from auth import get_current_user
from database import assignments_collection, assignment_helper, users_collection
from bson import ObjectId
from models import UserModel
from auth import verify_user
from schemas import RegisterSchema, LoginSchema
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(user: RegisterSchema):
    user_exist = await users_collection.find_one({"username": user.username})
    if user_exist:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    new_user = await users_collection.insert_one({
        "username": user.username,
        "password": hashed_password,
        "role": user.role,
    })
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(login: LoginSchema):
    user = await verify_user(login.username, login.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"token": str(user["_id"])}

@router.get("/assignments", dependencies=[Depends(get_current_user)])
async def get_assignments(current_user: UserModel = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    assignments = await assignments_collection.find({"admin": current_user["username"]}).to_list(100)
    return [assignment_helper(assignment) for assignment in assignments]

@router.post("/assignments/{id}/accept", dependencies=[Depends(get_current_user)])
async def accept_assignment(id: str, current_user: UserModel = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = await assignments_collection.update_one(
        {"_id": ObjectId(id), "admin": current_user["username"]},
        {"$set": {"status": "accepted"}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return {"message": "Assignment accepted"}

@router.post("/assignments/{id}/reject", dependencies=[Depends(get_current_user)])
async def reject_assignment(id: str, current_user: UserModel = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = await assignments_collection.update_one(
        {"_id": ObjectId(id), "admin": current_user["username"]},
        {"$set": {"status": "rejected"}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return {"message": "Assignment rejected"}

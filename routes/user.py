from fastapi import APIRouter, HTTPException, Depends
from models import UserModel, AssignmentModel
from database import users_collection, assignments_collection, user_helper
from auth import verify_user, get_current_user
from schemas import RegisterSchema, LoginSchema, UploadAssignmentSchema, UserRegistrationSchema
from passlib.context import CryptContext
from bson import ObjectId

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(user: UserRegistrationSchema):
    user_exist = await users_collection.find_one({"username": user.username})
    if user_exist:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    new_user = await users_collection.insert_one({
        "username": user.username,
        "password": hashed_password,
        "role": "user",
    })
    print(new_user.inserted_id)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(login: LoginSchema):
    user = await verify_user(login.username, login.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"token": str(user["_id"])}

@router.post("/upload", dependencies=[Depends(get_current_user)])
async def upload_assignment(assignment: UploadAssignmentSchema, current_user: UserModel = Depends(get_current_user)):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_assignment = AssignmentModel(userId=current_user["username"], task=assignment.task, admin=assignment.admin)
    await assignments_collection.insert_one(new_assignment.model_dump())
    return {"message": "Assignment uploaded successfully"}

@router.get("/admins", dependencies=[Depends(get_current_user)])
async def get_admins():
    admins = await users_collection.find({"role": "admin"}).to_list(100)
    return [user_helper(admin) for admin in admins]

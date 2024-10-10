from pydantic import BaseModel
from typing import Optional

class RegisterSchema(BaseModel):
    username: str
    password: str
    role: str

class UserRegistrationSchema(BaseModel):
    username: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

class UploadAssignmentSchema(BaseModel):
    task: str
    admin: str

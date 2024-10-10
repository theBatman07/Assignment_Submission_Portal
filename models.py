from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class UserModel(BaseModel):
    username: str
    password: str
    role: str

class AssignmentModel(BaseModel):
    userId: str
    task: str
    admin: str
    status: Optional[str] = "pending"
    timestamp: Optional[datetime] = datetime.now()

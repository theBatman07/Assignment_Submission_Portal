from fastapi import FastAPI
from routes import user, admin

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(admin.router, prefix="/admin")

# To run the app: uvicorn main:app --reload

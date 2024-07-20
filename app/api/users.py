from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate
from app.core.security import get_user_by_username
from app.db.database import users_collection
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(user: UserCreate):
    db_user = await get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = pwd_context.hash(user.password)
    user_data = {"username": user.username, "hashed_password": hashed_password}
    await users_collection.insert_one(user_data)
    return {"message": "User registered successfully"}

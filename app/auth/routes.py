from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth.schemas import Token
from app.auth.schemas import LoginRequest
from app.auth.schemas import UserCreate
from app.core.security import authenticate_user, create_access_token, verify_token, get_user_by_email
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.auth.models import User
from datetime import timedelta
from passlib.context import CryptContext
import uuid


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token", response_model=Token)
async def login_for_access_token(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = await authenticate_user(login_request.email, login_request.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-token/{token}")
async def verify_user_token(token: str):
    payload, email = verify_token(token=token)
    return {"message": "Token is valid", "email": email, "payload": payload}


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(id=str(uuid.uuid4()).replace('-', ''), name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

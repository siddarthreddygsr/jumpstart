from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.token import Token
from app.schemas.loginrequest import LoginRequest
from app.core.security import authenticate_user, create_access_token, verify_token
from datetime import timedelta


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login_for_access_token(login_request: LoginRequest):
    user = await authenticate_user(login_request.email, login_request.password)
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

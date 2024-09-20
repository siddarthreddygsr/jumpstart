from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    name: str
    password: str
    email: str


class User(UserCreate):
    id: str

    class Config:
        orm_mode = True

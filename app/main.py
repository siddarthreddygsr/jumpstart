from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router
import subprocess

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/host")
def host():
    result = subprocess.run(['hostname'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()


@app.get("/api/v2")
def version():
    return "0.1-loadtest1"


app.include_router(auth_router, prefix="/auth", tags=["auth"])

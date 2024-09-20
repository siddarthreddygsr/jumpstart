from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import app.constants.env_variables as env


DATABASE_URL = f"postgresql://{env.DB_USER}:{env.DB_PASS}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def user_helper(user) -> dict:
    return {
        "id": str(user.id),
        "email": user.email,
        "hashed_password": user.hashed_password
    }

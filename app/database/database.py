from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
load_dotenv(dotenv_path=".env")
DATABASE_URL = os.getenv("DATABASE_URL")
debug = os.getenv("DEBUG") == "True"
print(f"DATABASE_URL = {DATABASE_URL}")
print(f"DEBUG = {debug}")
# DATABASE_URL="postgresql://admin:0507@localhost:4406/shopeefood"
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
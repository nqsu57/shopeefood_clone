from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.model.user import User

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

# # Change password via email
# async def get_user_by_email(db: AsyncSession, email: str):
#     result = await db.execute(select(User).where(User.email == email))
#     return result.scalars().first()

# async def update_user_password(db: AsyncSession, email: str, new_hashed_password: str):
#     result = await db.execute(select(User).where(User.email == email))
#     user = result.scalars().first()
#     if user:
#         user.hashed_password = new_hashed_password
#         await db.commit()
#         await db.refresh(user)
#         return user
#     return None

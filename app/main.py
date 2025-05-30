from fastapi import FastAPI
from database.database import Base, engine, DATABASE_URL
from api.register import router

Base.metadata.create_all(bind=engine)
app = FastAPI()
# @app.get("/")
# async def root():
#     return {"message": "Hello S3"}
app.include_router(router, prefix="/api")
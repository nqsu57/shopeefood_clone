from fastapi import FastAPI
from app.database.database import Base, engine, DATABASE_URL
from app.api.register import router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()
# @app.get("/")
# async def root():
#     return {"message": "Hello Ss3"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

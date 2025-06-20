from fastapi import FastAPI
from app.database.database import Base, engine, DATABASE_URL
from app.api.register import router
from app.api.login import login_router
from app.api.get_user import get_user
from app.api.avatar import avatar_update
# from app.api.change_password import change_password_user
from app.api.update_profile import update_profile_router
from app.api.foods import foods, detail_food
from app.api.cart import cart_router
from fastapi.middleware.cors import CORSMiddleware
import app.model
# from app.api.send_email import forgot_password_router
# from app.api.send_email import reset_password_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
# @app.get("/")
# async def root():
#     return {"message": "Hello S3"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
app.include_router(login_router, prefix="/api")
app.include_router(get_user, prefix="/api")
app.include_router(update_profile_router, prefix="/api")
app.include_router(avatar_update, prefix="/api")
app.include_router(foods, prefix="/api")
app.include_router(detail_food, prefix="/api")
app.include_router(cart_router, prefix="/api")


# app.include_router(forgot_password_router, prefix="/api")
# app.include_router(reset_password_router, prefix="/api")

# app.include_router(change_password_user, prefix="/api")



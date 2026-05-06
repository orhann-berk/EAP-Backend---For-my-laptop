from fastapi import FastAPI
from database.database import engine
from routers import registration
from database.database import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(registration.router)

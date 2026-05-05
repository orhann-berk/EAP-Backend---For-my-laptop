from fastapi import FastAPI
from database.database import engine
from database import models
from routers import registration

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(registration.router)

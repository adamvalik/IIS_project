from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import Base, engine

from routers import scheduler
from routers import login
from routers import animals
from routers import users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(animals.router)
app.include_router(scheduler.router)
app.include_router(users.router)

# create tables in the database
Base.metadata.create_all(bind=engine)

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from db import Base, engine, get_db
from models import *

from routers import satecek_scheduler_mrdka
from routers import login
from routers import zviratka

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(satecek_scheduler_mrdka.router)
app.include_router(login.router)
app.include_router(zviratka.router)
app.include_router(satecek_scheduler_mrdka.router)

# create tables in the database
Base.metadata.create_all(bind=engine)

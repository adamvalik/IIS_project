from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from models import Animal

from routers import satecek_scheduler_mrdka
from routers import login
from routers import zviratka

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(satecek_scheduler_mrdka.router)
app.include_router(login.router)
app.include_router(zviratka.router)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from schemas import AnimalCreate, AnimalResponse  # Define Pydantic schemas for input/output

# Endpoint to create a new animal
@app.post("/animals/", response_model=AnimalResponse)
def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    db_animal = Animal(
        name=animal.name,
        species=animal.species,
        breed=animal.breed,
        birth_year=animal.birth_year,
        size=animal.size,
        description=animal.description,
    )
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

# Endpoint to fetch all animals
@app.get("/animals/", response_model=list[AnimalResponse])
def read_animals(db: Session = Depends(get_db)):
    return db.query(Animal).all()

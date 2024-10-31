# backend/schemas.py
from pydantic import BaseModel

class AnimalCreate(BaseModel):
    name: str
    species: str
    breed: str
    birth_year: int
    size: str
    description: str

class AnimalResponse(AnimalCreate):
    id: int

    class Config:
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy models

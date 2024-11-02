from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Animal as AnimalModel
from schemas import AnimalCreate as AnimalSchema
from db import get_db
import base64

router = APIRouter()

@router.get("/animal/{animal_id}", response_model=AnimalSchema)
async def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(AnimalModel).filter(AnimalModel.id == animal_id).first()
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

@router.get("/animals", response_model=List[AnimalSchema])
def get_animals(db: Session = Depends(get_db)):
    animals = db.query(AnimalModel).all()
    for animal in animals:
        if animal.photo:
            animal.photo = f"data:image/jpeg;base64,{base64.b64encode(animal.photo).decode()}"
    return animals

@router.get("/animals/recent", response_model=List[AnimalSchema])
async def get_recent_animals(db: Session = Depends(get_db)):
    recent_animals = db.query(AnimalModel).order_by(AnimalModel.admission_date.desc()).limit(3).all()
    for animal in recent_animals:
        if animal.photo:
            animal.photo = f"data:image/jpeg;base64,{base64.b64encode(animal.photo).decode()}"
    return recent_animals

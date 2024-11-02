from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Animal as AnimalModel
from schemas import Animal as AnimalSchema
from db import get_db
import base64

router = APIRouter()

@router.get("/animals/animal/{animal_id}", response_model=AnimalSchema)
async def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(AnimalModel).filter(AnimalModel.id == animal_id).first()
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")

    if animal.photo:
        animal.photo = f"data:image/jpeg;base64,{base64.b64encode(animal.photo).decode()}"
    return animal

@router.get("/animals", response_model=List[AnimalSchema])
async def get_animals(
    filter: Optional[str] = Query(None, description="Filter by species"),
    sort: Optional[str] = Query("name", description="Sort by field (name, age, species)"),
    db: Session = Depends(get_db)
):
    query = db.query(AnimalModel)
    if filter:
        query = query.filter(AnimalModel.species.ilike(f"%{filter}%"))

    if sort == "name":
        query = query.order_by(AnimalModel.name)
    elif sort == "age":
        query = query.order_by(AnimalModel.birth_year.desc())
    elif sort == "species":
        query = query.order_by(AnimalModel.species)

    animals = query.all()
    if not animals:
        raise HTTPException(status_code=404, detail="No animals found")

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

@router.get("/animals/species", response_model=List[str])
async def get_unique_species(db: Session = Depends(get_db)):
    species_list = db.query(AnimalModel.species).distinct().all()
    unique_species = [species[0] for species in species_list]

    if not unique_species:
        raise HTTPException(status_code=404, detail="No species found")

    return unique_species

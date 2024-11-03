from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Animal as AnimalModel
from schemas import Animal as AnimalSchema, AnimalCreate as AnimalCreateSchema
from db import get_db
from routers.login import verify_user
import base64

router = APIRouter()

@router.get("/addanimal")
async def addAnimal(user_verified: bool = Depends(verify_user)):
    if user_verified is None:
        raise HTTPException(status_code=401, detail="User not verified")
    
    if user_verified.get("role") not in ["admin", "caregiver"]:
        raise HTTPException(status_code=401, detail="User not authorized")
    
    return {"Validation successful"}

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

@router.post("/animals")
async def create_animal(animal: AnimalCreateSchema, db: Session = Depends(get_db)):
    try:
        photo_data = base64.b64decode(animal.photo) if animal.photo else None
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid photo format")

    new_animal = AnimalModel(
        name=animal.name,
        species=animal.species,
        breed=animal.breed,
        birth_year=animal.birth_year,
        photo=photo_data,
        admission_date=animal.admission_date,
        size=animal.size,
        caregivers_description=animal.caregivers_description,
        id_caregiver=animal.id_caregiver
    )
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)

@router.put("/animals/edit/{animal_id}")
async def update_animal(animal_id: int, animal: AnimalCreateSchema, db: Session = Depends(get_db)):
    animal_to_update = db.query(AnimalModel).filter(AnimalModel.id == animal_id).first()
    if animal_to_update is None:
        raise HTTPException(status_code=404, detail="Animal not found")

    animal_to_update.name = animal.name
    animal_to_update.species = animal.species
    animal_to_update.breed = animal.breed
    animal_to_update.birth_year = animal.birth_year
    animal_to_update.admission_date = animal.admission_date
    animal_to_update.size = animal.size
    animal_to_update.caregivers_description = animal.caregivers_description
    animal_to_update.id_caregiver = animal.id_caregiver

    db.commit()
    db.refresh(animal_to_update)

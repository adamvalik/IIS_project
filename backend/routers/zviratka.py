from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List


router = APIRouter()


# Example model for an animal
class Animal(BaseModel):
    id: int
    name: str
    species: str
    breed: str
    birth_year: int
    photo: str
    admission_date: str
    size: str
    description: str
    
class Reservation(BaseModel):
    day: str
    time: str

# Example data
animals = [
    Animal(
        id=1,
        name="Kwualedik",
        species="Dog",
        breed="DJ",
        birth_year=2015,
        photo="/assets/puppy.jpg",
        admission_date="2021-06-15",
        size="Large",
        description="Friendly and energetic."
    ),
    Animal(
        id=2,
        name="Max",
        species="Cat",
        breed="Siamese",
        birth_year=2018,
        photo="/assets/kotatko.jpg",
        admission_date="2022-01-10",
        size="Medium",
        description="Curious and playful."
    ),
    Animal(
        id=3,
        name="Charlie",
        species="Dog",
        breed="Beagle",
        birth_year=2017,
        photo="/assets/puppy.jpg",
        admission_date="2020-11-05",
        size="Medium",
        description="Loyal and affectionate."
    ),
    Animal(
        id=4,
        name="Luna",
        species="Rabbit",
        breed="Maine Coon",
        birth_year=2019,
        photo="/assets/rabbit.jpg",
        admission_date="2021-09-20",
        size="Large",
        description="Gentle and friendly."
    ),
    Animal(
        id=5,
        name="Rocky",
        species="Dog",
        breed="German Shepherd",
        birth_year=2016,
        photo="/assets/puppy.jpg",
        admission_date="2019-03-14",
        size="Large",
        description="Brave and intelligent."
    ),
    Animal(
        id=6,
        name="Satek",
        species="God",
        breed="Ing. Ph.D.",
        birth_year=-1274833874,
        photo="/assets/satek.jpg",
        admission_date="2019-03-14",
        size="Large",
        description="Circuitikz master."
    ),
    Animal(
        id=7,
        name="Bella",
        species="Dog",
        breed="Labrador Retriever",
        birth_year=2018,
        photo="/assets/puppy.jpg",
        admission_date="2021-05-10",
        size="Large",
        description="Friendly and outgoing."
    ),
    Animal(
        id=8,
        name="Oliver",
        species="Cat",
        breed="British Shorthair",
        birth_year=2020,
        photo="/assets/kotatko.jpg",
        admission_date="2022-02-15",
        size="Medium",
        description="Calm and affectionate."
    ),
    Animal(
        id=9,
        name="Daisy",
        species="Rabbit",
        breed="Lionhead",
        birth_year=2019,
        photo="/assets/rabbit.jpg",
        admission_date="2021-08-25",
        size="Small",
        description="Curious and playful."
    ),
    Animal(
        id=10,
        name="Milo",
        species="Dog",
        breed="Poodle",
        birth_year=2017,
        photo="/assets/puppy.jpg",
        admission_date="2020-12-01",
        size="Medium",
        description="Intelligent and active."
    ),
    Animal(
        id=11,
        name="Simba",
        species="Cat",
        breed="Maine Coon",
        birth_year=2016,
        photo="/assets/kotatko.jpg",
        admission_date="2019-07-20",
        size="Large",
        description="Gentle and friendly."
    ),
    Animal(
        id=12,
        name="Coco",
        species="Dog",
        breed="Chihuahua",
        birth_year=2021,
        photo="/assets/puppy.jpg",
        admission_date="2022-03-10",
        size="Small",
        description="Lively and bold."
    )
]

@router.get("/animal/{animal_id}", response_model=Animal)
async def get_animal(animal_id: int):
    animal = next((animal for animal in animals if animal.id == animal_id), None)
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

@router.get("/animals", response_model=List[Animal])
def get_animals():
    return animals

@router.get("/animals/recent", response_model=List[Animal])
async def get_recent_animals():
    return animals[-3:]

async def reserve_slots(reservations: List[Reservation]):
    return {"message": "Reservation successful!"}

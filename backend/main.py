from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example model for an animal
class Animal(BaseModel):
    id: int
    name: str
    description: str
    age: int
    type: str
    image: str

class Reservation(BaseModel):
    day: str
    time: str

# Example data
animals = [
    Animal(id=1, name="Bella", description="A playful young dog who loves attention.", age=3, type="Dog", image="https://placekitten.com/300/300"),
    Animal(id=2, name="Max", description="A friendly and curious cat.", age=2, type="Cat", image="https://placekitten.com/301/301"),
    Animal(id=3, name="Charlie", description="A gentle rabbit who loves to cuddle.", age=1, type="Rabbit", image="https://placekitten.com/302/302")
]

@app.get("/animals")
def get_animals():
    return animals

async def reserve_slots(reservations: List[Reservation]):
    return {"message": "Reservation successful!"}

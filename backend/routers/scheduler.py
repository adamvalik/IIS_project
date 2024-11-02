from fastapi import HTTPException, APIRouter
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Dict, List
import pytz

utc_now = datetime.now(pytz.utc)
local_tz = pytz.timezone('Europe/Prague')
utc_now = utc_now.astimezone(local_tz)
router = APIRouter()

class Slot(BaseModel):
    day: str
    time: str
    date: str

class ConfirmSelectionRequest(BaseModel):
    animalName: str
    slots: List[Slot]

# Static Data Definitions
users = [
    {
        "ID_user": 1,
        "email": "caregiver@example.com",
        "password": "hashedpassword",
        "name": "John",
        "surname": "Doe",
        "phone_num": "123456789",
        "role": "caregiver",
        "verified": True
    }
]

animals = [
    {
        "ID_animal": 1,
        "name": "Mr Mittens",
        "species": "Cat",
        "breed": "Siamese",
        "birth_year": 2015,
        "admission_date": datetime.now().date(),
        "size": "small",
        "caregivers_description": "Friendly and playful",
        "ID_caregiver": 1
    }
]

animal_borrows = [
    {
        "ID_borrow": 1,
        "date": datetime.now().date(),
        "time": utc_now,
        "borrowed": True,
        "returned": False,
        "ID_animal": 1
    }
]

reservations = [
    {
        "ID_reservation": 1,
        "approved": True,
        "ID_borrow": 1,
        "ID_volunteer": 1
    }
]

@router.get("/schedule/{animal_name}/{start_date}", response_model=dict)
async def get_schedule(animal_name: str, start_date: str):
    # Get the animal by name
    animal = next((a for a in animals if a["name"] == animal_name), None)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # Calculate week range
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = start_date + timedelta(days=6)

    # Get borrow data for the week
    borrows = [
        borrow for borrow in animal_borrows
        if borrow["ID_animal"] == animal["ID_animal"] and
           start_date <= borrow["date"] <= end_date
    ]
    print(borrows)

    # Create a dictionary to hold the schedule
    schedule: Dict[int, Dict[int, str]] = {day: {time: "blue" for time in range(9, 22)} for day in range(7)}
    print(schedule)

    for borrow in borrows:
        day_index = (borrow["date"] - start_date).days
        time_index = borrow["time"].hour
        print(day_index, time_index)
        if day_index >= 0 and time_index >= 0:
            schedule[day_index][time_index] = "red" if borrow["borrowed"] else "green"

    return {"schedule": schedule}

@router.get("/reserve/{animal_name}/{date}/{time}", response_model=dict)
async def reserve_slot(animal_name: str, date: str, time: str):
    # just return the input for now
    print("Reserve slot")
    return {"animal_name": animal_name, "date": date, "time": time}

@router.post("/confirmselection", response_model=Dict[str, str])
async def confirm_selection(request: ConfirmSelectionRequest):
    # Process the selected slots
    # TODO: check s databazi, jestli v mezicase zmena, tak error, jinak vse ok
    print("Confirming selection for:", request.animalName)
    for slot in request.slots:
        print(f"Day: {slot.day}, Time: {slot.time}, Date: {slot.date}")

    # Return a confirmation response
    return {"status": "success", "message": "Selection confirmed"}

@router.delete("/cancel/{animal_name}/{date}/{time}", response_model=dict)
async def cancel_slot(animal_name: str, date: str, time: str):
    # just return the input for now
    print("Cancel slot")
    return {"animal_name": animal_name, "date": date, "time": time}

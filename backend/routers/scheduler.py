from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from db import get_db
from typing import Dict, List
from schemas import ConfirmSelectionRequest, Slot
from models import Animal as AnimalModel
from models import AnimalBorrow as AnimalBorrowModel
from models import Reservation as ReservationModel
import pytz

# We be working in CR
utc_now = datetime.now(pytz.utc)
local_tz = pytz.timezone('Europe/Prague')
utc_now = utc_now.astimezone(local_tz)

router = APIRouter()

@router.get("/schedule/{animal_id}/{start_date}", response_model=dict)
async def get_schedule(animal_id: int, start_date: str, db: Session = Depends(get_db)):

    # Get the animal by name from the database
    animal = db.query(AnimalModel).filter(AnimalModel.id == animal_id).first()

    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # Calculate week range
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = start_date + timedelta(days=6)

    print(start_date, end_date)
    cast(start_date, Date)
    cast(end_date, Date)
    print(start_date, end_date)
    print(animal_id, animal.name)


    all_borrows = db.query(AnimalBorrowModel).all()
    print(f"All borrows: {[(borrow.date, borrow.time) for borrow in all_borrows]}")

    # Get borrow data for the week
    borrows = db.query(AnimalBorrowModel).filter(
        AnimalBorrowModel.id_animal == animal_id,
        cast(AnimalBorrowModel.date, Date) >= cast(start_date, Date),
        cast(AnimalBorrowModel.date, Date) <= cast(end_date, Date)
    ).all()

    print(borrows)

    if not borrows:
        print("No borrows found")

    # Create a dictionary to hold the schedule
    schedule: Dict[int, Dict[int, str]] = {day: {time: "gray" for time in range(9, 22)} for day in range(7)}
    print(schedule)

    for borrow in borrows:
        day_index = (borrow["date"] - start_date).days
        time_index = borrow["time"].hour
        print(day_index, time_index)
        if day_index >= 0 and time_index >= 0:
            schedule[day_index][time_index] = "blue" if borrow["borrowed"] else "green"

    return {"schedule": schedule}

@router.get("/reserve/{animal_name}/{date}/{time}", response_model=dict)
async def reserve_slot(animal_name: str, date: str, time: str, db: Session = Depends(get_db)):
    # just return the input for now
    print("Reserve slot")
    return {"animal_name": animal_name, "date": date, "time": time}

@router.post("/confirmselection", response_model=Dict[str, str])
async def confirm_selection(request: ConfirmSelectionRequest, db: Session = Depends(get_db)):
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

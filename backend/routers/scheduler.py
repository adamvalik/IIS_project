from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from db import get_db
from typing import Dict, List
from schemas import ConfirmSelectionRequest, Slot, CSlot, UADSlot
from models import Animal as AnimalModel
from models import AnimalBorrow as AnimalBorrowModel
from models import Reservation as ReservationModel
from routers.login import verify_user
import pytz

# We be working in CR
utc_now = datetime.now(pytz.utc)
local_tz = pytz.timezone('Europe/Prague')
utc_now = utc_now.astimezone(local_tz)

router = APIRouter()

@router.get("/scheduler")
async def listUsers(user_verified: bool = Depends(verify_user)):
    if user_verified is None:
        raise HTTPException(status_code=401, detail="User not verified")

    if user_verified.get("role") == "veterinarian":
        raise HTTPException(status_code=401, detail="User not authorized")
    # If the user is verified, return the list of users
    return {"Validation successful"}

@router.post("/schedule", response_model=dict)
async def get_schedule(uad_slot: UADSlot, db: Session = Depends(get_db)):

    user_id = uad_slot.user_id
    animal_id = uad_slot.animal_id
    start_date = utc_now.strftime("%Y-%m-%d")

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
    print(f"All borrows: {[(borrow.date, borrow.time, borrow.id_animal) for borrow in all_borrows]}")

    # Get borrow data for the week
    borrows = db.query(AnimalBorrowModel).filter(
        AnimalBorrowModel.id_animal == animal_id,
        AnimalBorrowModel.date >= start_date,
        AnimalBorrowModel.date <= end_date
    ).all()

    print(borrows)

    if not borrows:
        print("No borrows found")

    # Create a dictionary to hold the schedule
    schedule: Dict[int, Dict[int, str]] = {day: {time: "gray" for time in range(9, 22)} for day in range(7)}
    print(schedule)

    for borrow in borrows:
        my_reservation = False
        reservation_exists = False
        approved_reservation = False

        day_index = (borrow.date - start_date).days
        time_index = borrow.time.hour
        print(day_index, time_index)

        reservation = db.query(ReservationModel).filter(ReservationModel.id_borrow == borrow.id).first()

        if reservation:
            if reservation.id_volunteer == user_id:
                my_reservation = True
                if reservation.approved:
                    approved_reservation = True
                    my_reservation = False
            elif reservation.id_volunteer != user_id:
                reservation_exists = True

        if day_index >= 0 and time_index >= 0:
            if my_reservation:
                schedule[day_index][time_index] = "orange"
            elif reservation_exists:
                schedule[day_index][time_index] = "red"
            elif approved_reservation:
                schedule[day_index][time_index] = "green"
            else:
                schedule[day_index][time_index] = "blue"

    return {"schedule": schedule}


@router.post("/confirmselection", response_model=Dict[str, str])
async def confirm_selection(request: ConfirmSelectionRequest, db: Session = Depends(get_db)):
    print("Confirming selection for:", request.animal_id)

    for slot in request.slots:
        print(f"Day: {slot.day}, Time: {slot.time}, Date: {slot.date}")

        # Check if the `AnimalBorrow` already exists for this slot
        borrow = db.query(AnimalBorrowModel).filter(
            AnimalBorrowModel.id_animal == request.animal_id,
            AnimalBorrowModel.date == slot.date,
            AnimalBorrowModel.time == slot.time
        ).first()

        if borrow:
            # If a reservation already exists for this `AnimalBorrow`, raise an error
            if borrow.reservation:
                raise HTTPException(status_code=400, detail="Slot already reserved")

        # Create a new `Reservation` associated with this `AnimalBorrow`
        new_reservation = ReservationModel(
            approved=False,  # Assuming new reservations are not approved by default
            id_borrow=borrow.id,
            id_volunteer=request.user_id
        )
        db.add(new_reservation)

    try:
        db.commit()
        return {"status": "success", "message": "Selection confirmed"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error confirming selection: {e}")


@router.delete("/cancel/{user_id}/{animal_id}/{date}/{time}", response_model=dict)
async def cancel_slot(user_id: int, animal_id: int, date: str, time: str, db: Session = Depends(get_db)):

    borrow = db.query(AnimalBorrowModel).filter(
        AnimalBorrowModel.id_animal == animal_id,
        AnimalBorrowModel.date == date,
        AnimalBorrowModel.time == time
    ).first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Slot not found")

    reservation = db.query(ReservationModel).filter(
        ReservationModel.id_borrow == borrow.id,
        ReservationModel.id_volunteer == user_id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    db.delete(reservation)

    try:
        db.commit()
        return {"status": "success", "message": "Reservation cancelled"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error cancelling reservation: {e}")


@router.post("/createslot", response_model=dict)
async def create_slot(request: CSlot, db: Session = Depends(get_db)):

    for slot in request.new_slots:
        print(f"Day: {slot.day}, Time: {slot.time}, Date: {slot.date}")
        # Check if the `AnimalBorrow` already exists for this slot
        borrow = db.query(AnimalBorrowModel).filter(
            AnimalBorrowModel.id_animal == request.animal_id,
            AnimalBorrowModel.date == slot.date,
            AnimalBorrowModel.time == slot.time
        ).first()

        if borrow:
            # If a reservation already exists for this `AnimalBorrow`, raise an error
            if borrow.reservation:
                raise HTTPException(status_code=400, detail="Slot already reserved")

        new_borrow = AnimalBorrowModel(
            date=slot.date,
            time=slot.time,
            borrowed=False,
            returned=False,
            id_animal=request.animal_id
        )
        db.add(new_borrow)

    try:
        db.commit()
        return {"status": "success", "message": "Slot created"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating slot: {e}")

@router.delete('/delete/{animal_id}/{date}/{time}', response_model=dict)
async def delete_slot(animal_id: int, date: str, time: str, db: Session = Depends(get_db)):

    borrow = db.query(AnimalBorrowModel).filter(
        AnimalBorrowModel.id_animal == animal_id,
        AnimalBorrowModel.date == date,
        AnimalBorrowModel.time == time
    ).first()

    satek_flag = False
    # if there is a Reservation associated with this slot, delete it first
    if borrow.reservation:
        satek_flag = True
        db.delete(borrow.reservation)

    if not borrow:
        raise HTTPException(status_code=404, detail="Slot not found")

    db.delete(borrow)

    try:
        db.commit()
        if not satek_flag:
            return {"status": "success", "message": "Slot deleted"}
        else:
            return {"status": "success", "message": "Slot and associated reservation deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting slot: {e}")

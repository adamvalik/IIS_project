from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from db import get_db
from typing import Dict, List
from schemas import ConfirmSelectionRequest, Slot, CSlot, UADSlot, Reservation
from models import Animal as AnimalModel
from models import AnimalBorrow as AnimalBorrowModel
from models import Reservation as ReservationModel
from models import User as UserModel
from routers.login import verify_user, verify_volunteer_status, verify_user_role
import pytz

# We be working in CR
utc_now = datetime.now(pytz.utc)
local_tz = pytz.timezone('Europe/Prague')
utc_now = utc_now.astimezone(local_tz)

router = APIRouter(
    dependencies=[Depends(verify_user)]
)

@router.get("/scheduler/{id}")
async def listUsers(user_verified = Depends(verify_user), db: Session = Depends(get_db)):
    if user_verified.get("role") == "volunteer":
        verify_volunteer_status(user_verified.get("user_id"), db)
    return {"Validation successful"}

@router.post("/schedule", response_model=dict)
async def get_schedule(uad_slot: UADSlot, db: Session = Depends(get_db)):

    user_id = uad_slot.user_id
    animal_id = uad_slot.animal_id
    start_date = uad_slot.date

    # Get the animal by name from the database
    animal = db.query(AnimalModel).filter(AnimalModel.id == animal_id).first()

    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # Calculate week range
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = start_date + timedelta(days=6)

    cast(start_date, Date)
    cast(end_date, Date)

    all_borrows = db.query(AnimalBorrowModel).all()

    # Get borrow data for the week
    borrows = db.query(AnimalBorrowModel).filter(
        AnimalBorrowModel.id_animal == animal_id,
        AnimalBorrowModel.date >= start_date,
        AnimalBorrowModel.date <= end_date
    ).all()


    # Create a dictionary to hold the schedule
    schedule: Dict[int, Dict[int, str]] = {day: {time: "gray" for time in range(9, 22)} for day in range(7)}

    for borrow in borrows:
        my_reservation = False
        reservation_exists = False
        approved_reservation = False

        day_index = (borrow.date - start_date).days
        time_index = borrow.time.hour

        reservation = db.query(ReservationModel).filter(ReservationModel.id_borrow == borrow.id).first()
        role = db.query(UserModel).filter(UserModel.id == user_id).first().role

        if reservation and role != "caregiver":
            if reservation.id_volunteer == user_id:
                my_reservation = True
                if reservation.approved:
                    approved_reservation = True
                    my_reservation = False
            elif reservation.id_volunteer != user_id:
                reservation_exists = True

        if reservation and role == "caregiver":
            if reservation.approved:
                approved_reservation = True
            else:
                my_reservation = True

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


    for slot in request.slots:

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

    user_role = db.query(UserModel).filter(UserModel.id == user_id).first().role

    if user_role == "caregiver":
        if borrow.reservation:
            db.delete(borrow.reservation)
        else:
            raise HTTPException(status_code=404, detail="Reservation not found")
    else:
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
async def create_slot(request: CSlot, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver"])

    for slot in request.new_slots:
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

@router.get('/checkApproval/{animal_id}/{date}/{time}', response_model=dict)
async def check_approval(animal_id: int, date: str, time: str, db: Session = Depends(get_db)):

    borrow = db.query(AnimalBorrowModel).filter(
        AnimalBorrowModel.id_animal == animal_id,
        AnimalBorrowModel.date == date,
        AnimalBorrowModel.time == time
    ).first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Slot not found")

    if borrow.reservation:

        username = db.query(UserModel).filter(UserModel.id == borrow.reservation.id_volunteer).first().name + " " + db.query(UserModel).filter(UserModel.id == borrow.reservation.id_volunteer).first().surname

        if borrow.reservation.approved:

            return {'isApproved': True, 'username': username, 'user_id': borrow.reservation.id_volunteer}
        else:
            return {'isApproved': False, 'username': username, 'user_id': borrow.reservation.id_volunteer}
    else:
        # shouldnt happen really
        return {'isApproved': False, 'username': 'No one', 'user_id': -1}

@router.post('/approve', response_model=dict)
async def approve_slot(reservation: Reservation, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver"])

    borrow = db.query(AnimalBorrowModel).filter(
        AnimalBorrowModel.id_animal == reservation.animal_id,
        AnimalBorrowModel.date == reservation.date,
        AnimalBorrowModel.time == reservation.time
    ).first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Slot not found")

    if borrow.reservation:
        borrow.reservation.approved = True
    else:
        raise HTTPException(status_code=404, detail="Reservation not found")

    try:
        db.commit()
        return {"status": "success", "message": "Slot approved"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error approving slot: {e}")

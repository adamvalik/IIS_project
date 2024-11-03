from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session #, joinedload
from typing import List
from db import get_db
from models import Reservation as ReservationModel
from schemas import ReservationShow as ReservationSchema

router = APIRouter()

@router.get("/reservations", response_model=List[ReservationSchema])
async def get_all_reservations(db: Session = Depends(get_db)):
    reservations = db.query(ReservationModel).all()
    # reservations = (
    #     db.query(ReservationModel)
    #     .options(joinedload(ReservationModel.borrow), joinedload(ReservationModel.volunteer))
    #     .all()
    # )

    if not reservations:
        raise HTTPException(status_code=404, detail="No reservations found")
    return reservations

@router.get("/reservations/{user_id}", response_model=ReservationSchema)
async def get_user_reservations(user_id: int, db: Session = Depends(get_db)):
    user_reservations = db.query(ReservationModel).filter(ReservationModel.user_id == user_id).all()
    return user_reservations

@router.put("/reservations/{reservation_id}/toggle_borrowed")
async def update_borrowed_status(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    reservation.borrow.borrowed = not reservation.borrow.borrowed
    db.commit()
    return reservation

@router.put("/reservations/{reservation_id}/toggle_returned")
async def update_returned_status(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    reservation.borrow.returned = not reservation.borrow.returned
    db.commit()
    return reservation

@router.put("/reservations/{reservation_id}/approve")
async def approve_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    reservation.approved = True
    db.commit()
    return reservation

@router.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(reservation)
    db.commit()
    return {"message": "Reservation deleted successfully"}

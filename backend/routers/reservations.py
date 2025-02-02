from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import Reservation as ReservationModel
from schemas import ReservationShow as ReservationSchema
from routers.login import verify_user, verify_user_role, verify_volunteer_status, validate_same_user_id

router = APIRouter()

@router.get("/reservations", response_model=List[ReservationSchema])
async def get_all_reservations(db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver", "volunteer"])
    if(user_verified.get("role") == "volunteer"):
        verify_volunteer_status(user_verified.get("user_id"), db)

    # default - get all reservations sorted from the newest to the oldest
    reservations = db.query(ReservationModel).order_by(ReservationModel.id.desc()).all()
    return reservations

@router.get("/reservations/volunteer/{user_id}", response_model=List[ReservationSchema])
async def get_user_reservations(user_id: int, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver", "volunteer"])
    if(user_verified.get("role") == "volunteer"):
        verify_volunteer_status(user_verified.get("user_id"), db)

    user_reservations = db.query(ReservationModel).filter(ReservationModel.id_volunteer == user_id).order_by(ReservationModel.id.desc()).all()
    return user_reservations

@router.put("/reservations/{reservation_id}/toggle_borrowed")
async def update_borrowed_status(reservation_id: int, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver"])
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    reservation.borrow.borrowed = not reservation.borrow.borrowed
    db.commit()
    return reservation

@router.put("/reservations/{reservation_id}/toggle_returned")
async def update_returned_status(reservation_id: int, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver"])
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    reservation.borrow.returned = not reservation.borrow.returned
    db.commit()
    return reservation

@router.put("/reservations/{reservation_id}/approve")
async def approve_reservation(reservation_id: int, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver"])
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    reservation.approved = True
    db.commit()
    return reservation

@router.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver", "volunteer"])
    if(user_verified.get("role") == "volunteer"):
        verify_volunteer_status(user_verified.get("user_id"), db)
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(reservation)
    db.commit()
    return {"message": "Reservation deleted successfully"}

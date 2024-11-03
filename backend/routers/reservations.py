from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import Reservation as ReservationModel
from schemas import Reservation as ReservationSchema

router = APIRouter()

@router.get("/reservations", response_model=List[ReservationSchema])
async def get_all_reservations(db: Session = Depends(get_db)):
    reservations = db.query(ReservationModel).all()
    return reservations

@router.get("/reservations/{user_id}", response_model=ReservationSchema)
async def get_user_reservations(user_id: int, db: Session = Depends(get_db)):
    user_reservations = db.query(ReservationModel).filter(ReservationModel.user_id == user_id).all()
    return user_reservations


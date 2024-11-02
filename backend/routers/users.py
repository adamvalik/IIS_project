# main.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import User as UserModel
from schemas import User as UserSchema
router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users


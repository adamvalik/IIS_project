from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session #, joinedload
from typing import List
from db import get_db
from models import MedicalRecord as MedicalRecordModel
from models import Animal as AnimalModel
from models import User as UserModel

from schemas import MedicalRecord

router = APIRouter()

@router.get("/medical_records/{animal_id}", response_model=List[MedicalRecord])
async def get_medical_records(animal_id: int, db: Session = Depends(get_db)):
    records = db.query(MedicalRecordModel).filter(MedicalRecordModel.id_animal == animal_id).all()
    return records

@router.get("/medical_records/{record_id}", response_model=MedicalRecord)
async def get_medical_record_detail(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecordModel).filter(MedicalRecordModel.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

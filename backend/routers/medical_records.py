from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session #, joinedload
from typing import List
from db import get_db
from models import MedicalRecord as MedicalRecordModel
from models import Animal as AnimalModel
from models import User as UserModel
from routers.login import verify_user

from schemas import MedicalRecord, MedicalRecordGet

router = APIRouter(
    dependencies=[Depends(verify_user)]
)

@router.get("/medicalrecords/{record_id}")
async def validateRoute(record_id: int, user_verified = Depends(verify_user)):
    if (user_verified.get("role") == "volunteer"):
        raise HTTPException(status_code=401, detail="Volunteer not authorized")

    return {"Validation successful"}

@router.get("/all_medical_records", response_model=List[MedicalRecordGet])
async def get_all_medical_records(db: Session = Depends(get_db)):
    records = db.query(MedicalRecordModel).all()
    return records

@router.get("/medical_records/{animal_id}", response_model=List[MedicalRecordGet])
async def get_medical_records(animal_id: int, db: Session = Depends(get_db)):
    records = db.query(MedicalRecordModel).filter(MedicalRecordModel.id_animal == animal_id).all()
    return records

@router.get("/medical_record_get/{record_id}", response_model=MedicalRecordGet)
async def get_medical_record_detail(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecordModel).filter(MedicalRecordModel.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.post("/medical_records")
async def create_medical_record(record: MedicalRecord, db: Session = Depends(get_db)):
    new_record = MedicalRecordModel(
        date=record.date,
        weight=record.weight,
        vaccination=record.vaccination,
        vaccination_type=record.vaccination_type,
        vet_description=record.vet_description,
        id_animal=record.id_animal,
        id_veterinarian=record.id_veterinarian
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

@router.delete("/medical_record_delete/{record_id}")
async def delete_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecordModel).filter(MedicalRecordModel.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()

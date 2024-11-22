from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from typing import List
from schemas import VetRequest as VetRequestSchema, VetRequestShow as VetRequestShowSchema
from models import Animal as AnimalModel
from models import ExaminationRequest as ExaminationRequestModel
from routers.login import verify_user, verify_user_role

router = APIRouter()

@router.post("/request")
async def create_vet_request(vet_request: VetRequestSchema, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["caregiver", "admin"])

    animal_id = vet_request.animal_id
    caregivers_description = vet_request.request_text
    caregiver_id = vet_request.caregiver_id

    animal = db.query(AnimalModel).filter(AnimalModel.id == animal_id).first()

    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")

    vet_request = ExaminationRequestModel(
        caregivers_description=caregivers_description,
        id_animal=animal_id,
        id_caregiver=caregiver_id,
        id_veterinarian=None
    )

    db.add(vet_request)
    db.commit()
    db.refresh(vet_request)
    return {"message": "Request created successfully"}

@router.get("/requests", response_model=List[VetRequestShowSchema])
async def get_vet_requests(db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "veterinarian"])
    
    requests = db.query(ExaminationRequestModel).all()
    if not requests:
        raise HTTPException(status_code=404, detail="No requests found")
    return requests

@router.put("/requests/{request_id}/processed/{vet_id}")
async def process_request(request_id: int, vet_id: int, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "veterinarian"])
    request = db.query(ExaminationRequestModel).filter(ExaminationRequestModel.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    request.id_veterinarian = vet_id
    db.commit()


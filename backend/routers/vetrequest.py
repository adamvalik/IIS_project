from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from db import get_db
from typing import Dict, List
from schemas import VetRequest as VetRequestSchema
from models import Animal as AnimalModel
from models import ExaminationRequest as ExaminationRequestModel
from models import User as UserModel
from routers.login import verify_user
import pytz

router = APIRouter()

@router.post("/vetrequest", response_model=dict)
async def create_vet_request(
    vet_request: VetRequestSchema,
    db: Session = Depends(get_db)
):
    animal_id = vet_request.animal_id
    caregivers_description = vet_request.request_text
    caregiver_id = vet_request.caregiver_id

    animal = db.query(AnimalModel).filter(AnimalModel.id == animal_id).first()

    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")

    # if animal.id_caregiver != user.id:
    #     raise HTTPException(status_code=403, detail="You are not the caregiver of this animal")

    vet_request = ExaminationRequestModel(
        caregivers_description=caregivers_description,
        id_animal=animal_id,
        id_caregiver=caregiver_id
    )

    db.add(vet_request)
    db.commit()
    db.refresh(vet_request)
    return {"message": "Request created successfully"}

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date, time

# schemas for shared fields between create and update schemas
# examples:
class User(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    telephone: Optional[str] = None

    
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    access_token: str

class SignUpResponse(BaseModel):
    message: str

class Animal(BaseModel):
    id: int
    name: str
    species: str
    breed: Optional[str] = None
    birth_year: Optional[int] = None
    size: Optional[str] = Field(None, description="Size of the animal, e.g., small, medium, large")
    photo: Optional[bytes] = None
    admission_date: Optional[date] = None
    id_caregiver: int
    caregivers_description: Optional[str] = None

    class Config:
        orm_mode = True

class ExaminationRequestBase(BaseModel):
    caregivers_description: Optional[str] = None

class ExaminationRequestCreate(ExaminationRequestBase):
    id_animal: int
    id_caregiver: int

class ExaminationRequest(ExaminationRequestBase):
    id: int
    id_animal: int
    id_caregiver: int
    id_veterinarian: Optional[int] = None

    class Config:
        orm_mode = True

class MedicalRecordBase(BaseModel):
    date: Optional[date] = None
    weight: Optional[float] = None
    vaccination: Optional[bool] = None
    vaccination_type: Optional[str] = None
    vet_description: Optional[str] = None

class MedicalRecordCreate(MedicalRecordBase):
    id_animal: int
    id_veterinarian: int

class MedicalRecord(MedicalRecordBase):
    id: int
    id_animal: int
    id_veterinarian: int

    class Config:
        orm_mode = True

class AnimalBorrowBase(BaseModel):
    date: date
    time: time
    borrowed: Optional[bool] = None
    returned: Optional[bool] = None

class AnimalBorrowCreate(AnimalBorrowBase):
    id_animal: int

class AnimalBorrow(AnimalBorrowBase):
    id: int
    id_animal: int

    class Config:
        orm_mode = True

class ReservationBase(BaseModel):
    approved: Optional[bool] = None

class ReservationCreate(ReservationBase):
    id_borrow: int
    id_volunteer: int

class Reservation(ReservationBase):
    id: int
    id_borrow: int
    id_volunteer: int

    class Config:
        orm_mode = True

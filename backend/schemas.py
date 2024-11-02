from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date, time

# schemas for shared fields between create and update schemas
# examples:



class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str
    phone_num: Optional[str] = None
    role: Optional[str] = Field(None, description="Role of the user, e.g., caregiver, veterinarian, volunteer")

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    verified: Optional[bool] = False
    id_caregiver: Optional[int] = None

    class Config:
        orm_mode = True  # Enables reading from SQLAlchemy models

class AnimalBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    birth_year: Optional[int] = None
    size: Optional[str] = Field(None, description="Size of the animal, e.g., small, medium, large")

class AnimalCreate(AnimalBase):
    id_caregiver: int
    photo: Optional[bytes] = None
    admission_date: Optional[date] = None
    caregivers_description: Optional[str] = None

class Animal(AnimalBase):
    id: int
    id_caregiver: int

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

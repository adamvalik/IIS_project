from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time

class UserBase(BaseModel):
    name: str
    surname: str
    email: str

    class Config:
        orm_mode = True

class UserSignUp(UserBase):
    password: str
    phone: Optional[str] = None

class User(UserBase):
    id: int
    role: str
    phone: Optional[str] = None
    verified: Optional[bool] = None

class UserCreate(UserBase):
    role: str
    password: str

class UserUpdate(UserBase):
    role: str
    password: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    access_token: str

class SignUpResponse(BaseModel):
    message: str

class UpdatePhoneRequest(BaseModel):
    phone: str

class PasswordChangeRequest(BaseModel):
    oldPassword: str
    newPassword: str

    class Config:
        orm_mode = True

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

class AnimalCreate(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    birth_year: Optional[int] = None
    photo: Optional[str] = None
    admission_date: Optional[date] = None
    size: Optional[str] = Field(None, description="Size of the animal, e.g., small, medium, large")
    caregivers_description: Optional[str] = None
    id_caregiver: int

    class Config:
        orm_mode = True

class Slot(BaseModel):
    day: str
    time: str
    date: str

class ConfirmSelectionRequest(BaseModel):
    user_id: int
    animal_id: int
    slots: List[Slot]

class CSlot(BaseModel):
    animal_id: int
    new_slots: List[Slot]

class UADSlot(BaseModel):
    user_id: int
    animal_id: int
    date: str

class Reservation(BaseModel):
    animal_id: int
    date: str
    time: str

class ReservationShow(BaseModel):
    approved: bool
    borrow: object
    volunteer: object

    class Config:
        orm_mode = True

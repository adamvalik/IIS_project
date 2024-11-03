from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time

class UserBase(BaseModel):
    name: str
    surname: str
    email: str

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

class Slot(BaseModel):
    day: str
    time: str
    date: str

class ConfirmSelectionRequest(BaseModel):
    user_id: int
    animal_id: int
    slots: List[Slot]

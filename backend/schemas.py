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
    role: Optional[str] = Field(None, description="Role of the user, e.g., caregiver, veterinarian, volunteer")
    verified: Optional[bool] = False

    class Config:
        orm_mode = True

class UserWithId(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    password: Optional[str]
    role: Optional[str] = Field(None, description="Role of the user, e.g., caregiver, veterinarian, volunteer")
    verified: Optional[bool] = False

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


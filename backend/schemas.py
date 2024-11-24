from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time

class Token(BaseModel):
    mail: str
    role: str
    user_id: int

class RefreshResponse(BaseModel):
    access_token: str

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

class Veternarian(BaseModel):
    id: int
    name: str
    surname: str

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

#-------------------------------------------

class ReservationAnimal(BaseModel):
    id: int
    name: str

class ReservationUser(BaseModel):
    id: int
    name: str
    surname: str

    class Config:
        orm_mode = True

class ReservationAnimalBorrow(BaseModel):
    id: int
    date: date
    time: time
    borrowed: bool
    returned: bool
    animal: ReservationAnimal

    class Config:
        orm_mode = True

class ReservationShow(BaseModel):
    id: int
    approved: bool
    borrow: ReservationAnimalBorrow
    volunteer: ReservationUser

    class Config:
        orm_mode = True

#-------------------------------------------

class VetRequest(BaseModel):
    animal_id: int
    caregiver_id: int
    request_text: str

    class Config:
        orm_mode = True

class VetRequestShow(BaseModel):
    id: int
    caregivers_description: str
    animal: ReservationAnimal
    caregiver: ReservationUser
    id_veterinarian: Optional[int] = None

    class Config:
        orm_mode = True

#-------------------------------------------


class UserDetails(BaseModel):
    id: int

class MedicalRecord(BaseModel):
    date: date
    weight: float
    vaccination: bool
    vaccination_type: str
    vet_description: str
    id_animal: int
    id_veterinarian: int

class MedicalRecordGet(MedicalRecord):
    id: int

class EmailValidationRequest(BaseModel):
    email: str

# main.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import User as UserModel
from schemas import User as UserSchema, UserCreate as UserCreateSchema, UserUpdate as UserUpdateSchema, PasswordChangeRequest
from schemas import UpdatePhoneRequest
from routers.login import hash_password
from routers.login import verify_user, verify_password

router = APIRouter()

@router.get("/profile")
async def reachProfile(user_verified: bool = Depends(verify_user)):
    if user_verified is None:
        raise HTTPException(status_code=401, detail="User not verified")

    # If the user is verified, return the user's profile
    return {"Validation successful"}

@router.get("/listusers")
async def listUsers(user_verified: bool = Depends(verify_user)):
    if user_verified is None:
        raise HTTPException(status_code=401, detail="User not verified")

    role = user_verified.get("role")
    if role not in ["admin", "caregiver"]:
        raise HTTPException(status_code=401, detail="User not authorized")

    # If the user is verified, return the list of users
    return {"Validation successful"}

@router.get("/users", response_model=List[UserSchema])
async def get_all_users(db: Session = Depends(get_db)):
    # retrieve all users except the admin
    admin_user = db.query(UserModel).order_by(UserModel.id.asc()).first()
    users = db.query(UserModel).filter(UserModel.id != admin_user.id).all()
    return users

@router.get("/volunteers", response_model=List[UserSchema])
async def get_volunteers(db: Session = Depends(get_db)):
    volunteers = db.query(UserModel).filter(UserModel.role == "volunteer").all()
    return volunteers

@router.post("/users")
async def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):

    if(db.query(UserModel).filter(UserModel.email == user.email).first() is not None):
        raise HTTPException(status_code=400, detail="User already exists.")

    new_user = UserModel(
        email=user.email,
        password=hash_password(user.password),
        name=user.name,
        surname=user.surname,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    print(user_id)

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdateSchema, db: Session = Depends(get_db)):
    user_to_update = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found.")

    user_to_update.email = user.email
    user_to_update.name = user.name
    user_to_update.surname = user.surname
    user_to_update.role = user.role
    if user.password:
        user_to_update.password = hash_password(user.password)
    db.commit()

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(user_to_delete)
    db.commit()

@router.put("/volunteers/{volunteer_id}/verify")
async def verify_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    volunteer = db.query(UserModel).filter(UserModel.id == volunteer_id).first()
    if volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found.")
    volunteer.verified = True
    db.commit()

@router.put("/users/{user_id}/phone")
async def update_phone(user_id: int, request: UpdatePhoneRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    user.phone = request.phone
    db.commit()

@router.put("/users/{user_id}/password")
async def change_password(user_id: int, request: PasswordChangeRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    if not verify_password(request.oldPassword, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    user.password = hash_password(request.newPassword)
    db.commit()

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import User as UserModel
from schemas import User as UserSchema, UserCreate as UserCreateSchema, UserUpdate as UserUpdateSchema, PasswordChangeRequest
from schemas import UpdatePhoneRequest, UserDetails, Veternarian as VeternarianSchema, EmailValidationRequest
from routers.login import hash_password
from routers.login import verify_user, verify_password, verify_user_role, validate_same_user_id

router = APIRouter(
    dependencies=[Depends(verify_user)]
)

@router.get("/profile")
async def reachProfile():
    # If the user is verified, return the user's profile
    return {"Validation successful"}

@router.get("/listusers")
async def listUsers(user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver"])
    # If the user is verified, return the list of users
    return {"Validation successful"}

@router.get("/users", response_model=List[UserSchema])
async def get_all_users(db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin"])
    # retrieve all users except the admin
    admin_user = db.query(UserModel).order_by(UserModel.id.asc()).first()
    users = db.query(UserModel).filter(UserModel.is_deleted == False).filter(UserModel.id != admin_user.id).all()
    return users

@router.get("/volunteers", response_model=List[UserSchema])
async def get_volunteers(db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver"])
    volunteers = db.query(UserModel).filter(UserModel.is_deleted == False).filter(UserModel.role == "volunteer").all()
    return volunteers

@router.post("/users")
async def create_user(user: UserCreateSchema, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver"])
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

@router.put("/volunteers/{volunteer_id}/verify")
async def verify_volunteer(volunteer_id: int, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    verify_user_role(user_verified, ["admin", "caregiver"])
    volunteer = db.query(UserModel).filter(UserModel.id == volunteer_id).first()
    if volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found.")
    volunteer.verified = True
    db.commit()

@router.get("/users/volunteers/{volunteer_id}/verify")
async def check_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    volunteer = db.query(UserModel).filter(UserModel.id == volunteer_id).first()
    if volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found.")
    return volunteer.verified

@router.put("/users/{user_id}/phone")
async def update_phone(user_id: int, request: UpdatePhoneRequest, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    if(user_verified.get("role") != "admin"):
        validate_same_user_id(user_id, user_verified.get("user_id"))
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    user.phone = request.phone
    db.commit()

@router.put("/users/{user_id}/password")
async def change_password(user_id: int, request: PasswordChangeRequest, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    if(user_verified.get("role") != "admin"):
        validate_same_user_id(user_id, user_verified.get("user_id"))
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    if not verify_password(request.oldPassword, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    user.password = hash_password(request.newPassword)
    db.commit()

@router.post("/user_detail", response_model=dict)
async def get_user_details(ida: UserDetails, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == ida.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    name = user.name
    surname = user.surname
    email = user.email
    phone = user.phone
    role = user.role
    return {"name": name, "surname": surname, "mail": email, "telephone": phone, "role": role}

@router.get("/user/{user_id}")
async def reachProfile(user_id: int, user_verified = Depends(verify_user)):
    if(user_verified.get("role") == "volunteer" or user_verified.get("role") == "veterinarian"):
        validate_same_user_id(user_id, user_verified.get("user_id"))

    return {"Validation successful"}

@router.get("/vet/{vet_id}", response_model=VeternarianSchema)
async def get_vet(vet_id: int, db: Session = Depends(get_db)):
    vet = db.query(UserModel).filter(UserModel.id == vet_id).first()
    if vet is None:
        raise HTTPException(status_code=404, detail="Veterinarian not found.")
    return vet

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), user_verified = Depends(verify_user)):
    if(user_verified.get("role") != "admin" and user_verified.get("role") != "caregiver"):
        validate_same_user_id(user_id, user_verified.get("user_id"))

    user_to_delete = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if(user_verified.get("role") == "caregiver"):
        if(user_to_delete.role != "volunteer" and (user_to_delete.id != user_verified.get("user_id"))):
            raise HTTPException(status_code=403, detail="You cannot delete other people than volunteers.")

    user_to_delete.is_deleted = True
    db.commit()

@router.get("/users/{user_id}/is_deleted", response_model=bool)
async def is_user_deleted(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.is_deleted

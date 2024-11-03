from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from jose import JWTError, jwt
from enum import Enum
from datetime import datetime, timedelta, timezone
from schemas import UserSignUp as UserSchema, LoginRequest, LoginResponse, SignUpResponse
from sqlalchemy.orm import Session
from models import User as UserModel
from db import get_db

SECRET_KEY = "rogalo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         # Decode the JWT token using the secret key and algorithm
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         # Extract information from the payload
#         email = payload.get("sub")
#         role = payload.get("role")
#         user_id = payload.get("user_id")

#         # Check if all necessary fields are present
#         if email is None or role is None or user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid credentials")

#         # Return user details as a dictionary
#         return {"email": email, "role": role, "user_id": user_id}

#     except JWTError:
#         # Raise an HTTP exception if there's an error in decoding the JWT
#         raise HTTPException(status_code=403, detail="Could not validate credentials")

def verify_user(token: str = Depends(oauth2_scheme)) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        user_id = payload.get("user_id")

        # Check if essential information is present
        if email is None or role is None or user_id is None:
            return False  # Return False if verification fails

        return True  # Return True if verification is successful
    except JWTError:
        return False  # Return False if token is invalid

@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):

    userFound = None
    if(db.query(UserModel).filter(UserModel.email == login_request.email).first() is not None):
        userFound = db.query(UserModel).filter(UserModel.email == login_request.email).first()

    if userFound is None:
        raise HTTPException(status_code=401, detail="User not found.")

    if not verify_password(login_request.password, userFound.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "sub": userFound.email,
        "role": userFound.role,
        "user_id": userFound.id,
        "tokenExp": ACCESS_TOKEN_EXPIRE_MINUTES,
    }

    access_token = create_access_token(data=token_data)

    return {"message": "Login successful", "access_token": access_token}

@router.post("/signup", response_model=SignUpResponse)
async def create_user(user: UserSchema, db: Session = Depends(get_db)):

    if(db.query(UserModel).filter(UserModel.email == user.email).first() is not None):
        raise HTTPException(status_code=400, detail="User already exists.")

    new_user = UserModel(
        email=user.email,
        password=hash_password(user.password),
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        role="volunteer"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return SignUpResponse(message="User created successfully")

from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from jose import JWTError, jwt
from enum import Enum
from datetime import datetime, timedelta, timezone
from schemas import UserSignUp as UserSchema, LoginRequest, LoginResponse, SignUpResponse, Token, RefreshResponse, EmailValidationRequest
from sqlalchemy.orm import Session
from models import User as UserModel
from db import get_db

# Define a dependency for bearer token authentication
Oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

# Function to create an access token
def create_user_token(user_id: int, userMail: str, userRole: str):
    tokendata = {
        "mail": userMail,
        "role": userRole,
        "user_id": user_id
    }
    #Add a 10 minute expiration time to the token
    expireTokenTime = datetime.now(timezone.utc) + timedelta(minutes=10)
    tokendata.update({"exp": expireTokenTime})
    return jwt.encode(tokendata, "rogalo", algorithm="HS256")

# Function to hash a password using bcrypt and salt to add security
def hash_password(password: str) -> str:
    bytePassword = password.encode('utf-8')
    hashedPassword = bcrypt.hashpw(bytePassword, bcrypt.gensalt())
    byteHashedPassword = hashedPassword.decode('utf-8')
    return byteHashedPassword

# Function to verify a password using bcrypt
def verify_password(password: str, hashed_password: str) -> bool:
    bytePassword = password.encode('utf-8')
    byteHashedPassword = hashed_password.encode('utf-8')
    return bcrypt.checkpw(bytePassword, byteHashedPassword)

# Function that verifies the user's token and looking up the user in the database
def verify_user(token: str = Depends(Oauth2Scheme), db: Session = Depends(get_db)):
    try:
        decodedToken = jwt.decode(token, "rogalo", algorithms=["HS256"])
        email = decodedToken.get("mail")
        role = decodedToken.get("role")
        user_id = decodedToken.get("user_id")

        userFound = db.query(UserModel).filter(UserModel.email == email).first()
        
        if userFound is None or userFound.id != user_id or userFound.role != role:
            raise HTTPException(status_code=401, detail="User not verified")

        return decodedToken
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
# Function that verifies the user's role
def verify_user_role(decodedToken: dict, roles: List[str]):
    if decodedToken.get("role") not in roles:
        raise HTTPException(status_code=401, detail=f'User with role {decodedToken.get("role")} not authorized')
    
# Function that verifies  if the user is a verified volunteer
def verify_volunteer_status(user_id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.verified:
        raise HTTPException(status_code=401, detail="Volunteer not verified")
    
# Function that validates if the user is asking for their own data
def validate_same_user_id(user_id: int, actual_user_id: int):
    if user_id != actual_user_id:
        raise HTTPException(status_code=401, detail="User asks for different user's data")
        
# Function that creates a new token with updated expiration time
@router.post("/refresh-token-interval", response_model=RefreshResponse)
async def resfreshTokenInterval(token: Token):
    access_token = create_user_token(token.user_id, token.mail, token.role)
    return {"access_token": access_token}

@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):

    userFound = None
    if(db.query(UserModel).filter(UserModel.email == login_request.email).first() is not None):
        userFound = db.query(UserModel).filter(UserModel.email == login_request.email).first()

    if userFound is None:
        raise HTTPException(status_code=401, detail="User not found.")

    if not verify_password(login_request.password, userFound.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_user_token(userFound.id, userFound.email, userFound.role)

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

@router.post("/email_validation", response_model=bool)
async def validate_email(request: EmailValidationRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == request.email).first()
    #true if email is in use, false if not
    return user is not None

from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from jose import JWTError, jwt
from enum import Enum
from datetime import datetime, timedelta

SECRET_KEY = "rogalo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


current_free_id = 3

class UserRole(Enum):
    caregiver = "caregiver"
    veterinarian = "veterinarian"
    volunteer = "volunteer"


class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    access_token: str

class SignUpResponse(BaseModel):
    message: str

class User(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    telephone: Optional[str] = None
    id: int
    role: Optional[UserRole] = None

users = [
    User(id=1, email="user1@example.com", password=hash_password("auticko"), name="John", surname="Doe", telephone="123456789", role=UserRole.caregiver),
    User(id=2, email="user2@example.com", password=hash_password("mypassword123"), name="Jane", surname="Doe", telephone="987654321", role=UserRole.veterinarian),
]

# Dependency to retrieve user and validate role
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        user_id = payload.get("user_id") 

        if email is None or role is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return {"email": email, "role": role, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")


@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    # Dummy validation logic
    userFound = None

    for user in users:
        if user.email == login_request.email:
            userFound = user
            break
    
    if userFound is None:
        raise HTTPException(status_code=401, detail="User not found.")
    
    if not verify_password(login_request.password, userFound.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {
        "sub": userFound.email,
        "role": userFound.role.value,
        "user_id": userFound.id
    }

    access_token = create_access_token(data=token_data)
    
    return {"message": "Login successful", "access_token": access_token}

@router.post("/signup", response_model=SignUpResponse)
async def create_user(user: User):
    global current_free_id

    for existing_user in users:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="User already exists.")

    user.password = hash_password(user.password)
    user.id = current_free_id
    user.role = UserRole.volunteer

    users.append(user)
    current_free_id += 1
    return SignUpResponse(message="User created successfully")
    



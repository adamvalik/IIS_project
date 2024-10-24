from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vue.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# Sample data class
# class User:
#     def __init__(self, id: int, email: str, password: str, name: str, surname: str, telephone: str=None):
#         self.id = id
#         self.email = email
#         self.password = password
#         self.name = name
#         self.surname = surname
#         self.telephone = telephone

# # Testing data
# users = [
#     User(id=1, email="user1@example.com", password=hash_password("auticko"), name="John", surname="Doe", telephone="123456789"),
#     User(id=2, email="user2@example.com", password=hash_password("mypassword123"), name="Jane", surname="Doe", telephone="987654321"),
# ]

current_free_id = 3

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str

# class NewUser(BaseModel):
#     email: str
#     password: str
#     name: str
#     surname: str
#     telephone: Optional[str] = None

class User(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    telephone: Optional[str] = None
    id: int

users = [
    User(id=1, email="user1@example.com", password=hash_password("auticko"), name="John", surname="Doe", telephone="123456789"),
    User(id=2, email="user2@example.com", password=hash_password("mypassword123"), name="Jane", surname="Doe", telephone="987654321"),
]


@app.post("/login", response_model=LoginResponse)
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
    return LoginResponse(message="Login successful")

@app.post("/signup", response_model=LoginResponse)
async def create_user(user: User):
    global current_free_id

    for existing_user in users:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="User already exists.")

    user.password = hash_password(user.password)
    user.id = current_free_id

    users.append(user)
    current_free_id += 1
    return LoginResponse(message="User created successfully")
    



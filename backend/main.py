from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from routers import login
from example_data import create_example_users, create_example_animals

from db import Base, engine
from contextlib import asynccontextmanager

from routers import scheduler
from routers import login
from routers import animals
from routers import users
from routers import vetrequest
from routers import reservations
from routers import medical_records

# URL = "http://localhost:8000"


# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Check if the requested route requires authentication
#         protected_routes = ['/profile']
#         if request.url.path in protected_routes:
#             token = request.headers.get('Authorization')
#             if not token or not login.verify_user(token):
#                 raise HTTPException(status_code=401, detail="Unauthorized")

#         # Call the next middleware or route handler
#         response = await call_next(request)

#         # Optionally modify the response here

#         return response  # Return the response back to the client



# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     user_ids = create_example_users()
#     animal_ids = create_example_animals(user_ids)
#     yield 

# app = FastAPI(lifespan=lifespan)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(AuthMiddleware)

app.include_router(login.router)
app.include_router(animals.router)
app.include_router(scheduler.router)
app.include_router(users.router)
app.include_router(reservations.router)
app.include_router(vetrequest.router)
app.include_router(medical_records.router)

# create tables in the database
Base.metadata.create_all(bind=engine)

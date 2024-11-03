from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from routers import login

from db import Base, engine

from routers import scheduler
from routers import login
from routers import animals
from routers import users

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

# create tables in the database
Base.metadata.create_all(bind=engine)

from fastapi import HTTPException, APIRouter
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Time, ForeignKey, Enum, BLOB, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

#fastapi.middleware.cors import CORSMiddleware

# router = APIRouter()

# # Database Setup
# DATABASE_URL = "mysql+mysqlconnector://root:koteseni@localhost/utulek"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "User"
    ID_user = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    phone_num = Column(String(20))
    role = Column(Enum('caregiver', 'veterinarian', 'volunteer'))
    verified = Column(Boolean)
    ID_caregiver = Column(Integer, ForeignKey("User.ID_user"))

class Animal(Base):
    __tablename__ = "Animal"
    ID_animal = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    species = Column(String(255), nullable=False)
    breed = Column(String(255))
    birth_year = Column(Integer)
    photo = Column(BLOB)
    admission_date = Column(Date)
    size = Column(Enum('small', 'medium', 'large'))
    caregivers_description = Column(Text)
    ID_caregiver = Column(Integer, ForeignKey("User.ID_user"))

# class AnimalBorrow(Base):
#     __tablename__ = "Animal_borrow"
#     ID_borrow = Column(Integer, primary_key=True, index=True)
#     date = Column(Date, nullable=False)
#     time = Column(Time, nullable=False)
#     borrowed = Column(Boolean, default=False)
#     returned = Column(Boolean, default=False)
#     ID_animal = Column(Integer, ForeignKey("Animal.ID_animal"))

# class Reservation(Base):
#     __tablename__ = "Reservation"
#     ID_reservation = Column(Integer, primary_key=True, index=True)
#     approved = Column(Boolean, default=False)
#     ID_borrow = Column(Integer, ForeignKey("Animal_borrow.ID_borrow"))
#     ID_volunteer = Column(Integer, ForeignKey("User.ID_user"))

# Base.metadata.create_all(bind=engine)

# # Helper functions to insert initial data
# def insert_initial_data():
#     session = SessionLocal()

#     # Insert caregiver user data
#     user = User(
#         email="caregiver@example.com",
#         password="hashedpassword",
#         name="John",
#         surname="Doe",
#         phone_num="123456789",
#         role="caregiver",
#         verified = True
#     )
#     session.add(user)
#     session.commit()  # Commit to get the ID

#     # Insert some animal data, associating it with the caregiver
#     animal = Animal(
#         name="Mr Mittens",
#         species="Cat",
#         breed="Siamese",
#         birth_year=2015,
#         admission_date=datetime.now().date(),
#         size="small",
#         caregivers_description="Friendly and playful",
#         ID_caregiver=user.ID_user
#     )
#     session.add(animal)
#     session.commit()

#     # Insert an animal borrow record
#     animal_borrow = AnimalBorrow(
#         date=datetime.now().date(),
#         time=datetime.now().time(),
#         borrowed=True,
#         returned=False,
#         ID_animal=animal.ID_animal
#     )
#     session.add(animal_borrow)
#     session.commit()

#     # Insert a reservation
#     reservation = Reservation(
#         approved=True,
#         ID_borrow=animal_borrow.ID_borrow,
#         ID_volunteer=user.ID_user
#     )
#     session.add(reservation)
#     session.commit()

#     session.close()

# insert_initial_data()

# @router.get("/schedule/{animal_name}/{start_date}")
# async def get_schedule(animal_name: str, start_date: str):
#     session = SessionLocal()

#     # Get the animal by name
#     animal = session.query(Animal).filter(Animal.name == animal_name).first()
#     if not animal:
#         raise HTTPException(status_code=404, detail="Animal not found")

#     # Calculate week range
#     start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#     end_date = start_date + timedelta(days=6)

#     # Get borrow data for the week
#     borrows = session.query(AnimalBorrow).filter(
#         AnimalBorrow.ID_animal == animal.ID_animal,
#         AnimalBorrow.date >= start_date,
#         AnimalBorrow.date <= end_date
#     ).all()

#     # Create a dictionary to hold the schedule
#     schedule = {day: {time: "blue" for time in range(9, 22)} for day in range(7)}

#     for borrow in borrows:
#         day_index = (borrow.date - start_date).days
#         time_index = borrow.time.hour - 9
#         if day_index >= 0 and time_index >= 0:
#             schedule[day_index][time_index] = "red" if borrow.borrowed else "green"

#     return {"schedule": schedule}

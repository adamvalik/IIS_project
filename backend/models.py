# backend/models.py
from sqlalchemy import Column, Integer, String
from db import Base

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))         
    species = Column(String(50))       
    breed = Column(String(50))         
    description = Column(String(255))  
    size = Column(String(20))          
    birth_year = Column(Integer)

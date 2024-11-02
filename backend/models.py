# translation of /doc/tables.sql to SQLAlchemy ORM
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum, Text, DECIMAL, Time
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column("ID_user", Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    phone_num = Column(String(20), nullable=True)
    role = Column(Enum('caregiver', 'veterinarian', 'volunteer', 'admin'), nullable=False)

    # volunteer specific
    verified = Column(Boolean, nullable=True)

    animals = relationship("Animal", back_populates="caregiver")
    examination_requests_as_caregiver = relationship("ExaminationRequest", back_populates="caregiver", foreign_keys="[ExaminationRequest.id_caregiver]")
    examination_requests_as_vet = relationship("ExaminationRequest", back_populates="veterinarian", foreign_keys="[ExaminationRequest.id_veterinarian]")
    medical_records = relationship("MedicalRecord", back_populates="veterinarian")
    reservations = relationship("Reservation", back_populates="volunteer")

class Animal(Base):
    __tablename__ = "animals"

    id = Column("ID_animal", Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    species = Column(String(255), nullable=False)
    breed = Column(String(255), nullable=True)
    birth_year = Column(Integer, nullable=True)
    photo = Column(MEDIUMBLOB, nullable=True)
    admission_date = Column(Date, nullable=True)
    size = Column(Enum('small', 'medium', 'large'), nullable=True)
    caregivers_description = Column(Text, nullable=True)
    id_caregiver = Column(Integer, ForeignKey("users.ID_user"), nullable=False)

    caregiver = relationship("User", back_populates="animals")
    examination_requests = relationship("ExaminationRequest", back_populates="animal")
    medical_records = relationship("MedicalRecord", back_populates="animal")
    borrows = relationship("AnimalBorrow", back_populates="animal")

class ExaminationRequest(Base):
    __tablename__ = "examination_requests"

    id = Column("ID_request", Integer, primary_key=True, autoincrement=True)
    caregivers_description = Column(Text, nullable=True)
    id_animal = Column(Integer, ForeignKey("animals.ID_animal"), primary_key=True)
    id_caregiver = Column(Integer, ForeignKey("users.ID_user"), nullable=False)
    id_veterinarian = Column(Integer, ForeignKey("users.ID_user"), nullable=True)

    animal = relationship("Animal", back_populates="examination_requests")
    caregiver = relationship("User", back_populates="examination_requests_as_caregiver", foreign_keys=[id_caregiver])
    veterinarian = relationship("User", back_populates="examination_requests_as_vet", foreign_keys=[id_veterinarian])

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column("ID_record", Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=True)
    weight = Column(DECIMAL(5, 2), nullable=True)
    vaccination = Column(Boolean, nullable=True)
    vaccination_type = Column(String(255), nullable=True)
    vet_description = Column(Text, nullable=True)
    id_animal = Column(Integer, ForeignKey("animals.ID_animal"), primary_key=True)
    id_veterinarian = Column(Integer, ForeignKey("users.ID_user"), nullable=False)

    animal = relationship("Animal", back_populates="medical_records")
    veterinarian = relationship("User", back_populates="medical_records")

class AnimalBorrow(Base):
    __tablename__ = "animal_borrows"

    id = Column("ID_borrow", Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    borrowed = Column(Boolean, nullable=True)
    returned = Column(Boolean, nullable=True)
    id_animal = Column(Integer, ForeignKey("animals.ID_animal"), nullable=False)

    animal = relationship("Animal", back_populates="borrows")
    reservation = relationship("Reservation", back_populates="borrow", uselist=False)

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column("ID_reservation", Integer, primary_key=True, autoincrement=True)
    approved = Column(Boolean, nullable=True)
    id_borrow = Column(Integer, ForeignKey("animal_borrows.ID_borrow"), nullable=False)
    id_volunteer = Column(Integer, ForeignKey("users.ID_user"), nullable=False)

    borrow = relationship("AnimalBorrow", back_populates="reservation")
    volunteer = relationship("User", back_populates="reservations")

from datetime import date, time
from db import SessionLocal
from models import User, Animal, ExaminationRequest, MedicalRecord, AnimalBorrow, Reservation
from routers import login
import os

IMAGE_DIRECTORY = "./images"

def load_image_as_binary(image_name):
    file_path = os.path.join(IMAGE_DIRECTORY, image_name)
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

def create_example_users():
    users = [
        User(email="admin@admin.com", password=login.hash_password("admin"), name="Admin", surname="Admin", phone="0000000000", role="admin"),
        User(email="caregiver@example.com", password=login.hash_password("password"), name="Bob", surname="Caregiver", phone="1234567890", role="caregiver"),
        User(email="vet@example.com", password=login.hash_password("password12"), name="Dr. Alice", surname="Veterinarian", phone="0987654321", role="veterinarian"),
        User(email="volunteer@example.com", password=login.hash_password("password123"), name="Charlie", surname="Volunteer", phone="1122334455", role="volunteer", verified=True)
    ]
    db = SessionLocal()
    try:
        db.add_all(users)
        db.commit()
        print("Example users added to the database.")

        return {user.role: user.id for user in db.query(User).all()}
    except Exception as e:
        db.rollback()
        print(f"Error adding example users: {e}")
    finally:
        db.close()

def create_example_animals(user_ids):
    caregiver_id = user_ids.get("caregiver")
    animals = [
        Animal(
            name="Bella", species="Dog", breed="Labrador Retriever", birth_year=2018,
            photo=load_image_as_binary("puppy.jpg"), admission_date=date(2021, 5, 10),
            size="large", caregivers_description="Friendly and outgoing.", id_caregiver=caregiver_id
        ),
        Animal(
            name="Mittens", species="Cat", breed="Siamese", birth_year=2016,
            photo=load_image_as_binary("kotatko.jpg"), admission_date=date(2022, 3, 8),
            size="medium", caregivers_description="Quiet and affectionate.", id_caregiver=caregiver_id
        ),
    ]

    db = SessionLocal()
    try:
        db.add_all(animals)
        db.commit()
        print("Example animals added to the database.")

        return {animal.name: animal.id for animal in db.query(Animal).all()}
    except Exception as e:
        db.rollback()
        print(f"Error adding example animals: {e}")
    finally:
        db.close()

def create_example_examination_requests(user_ids, animal_ids):
    caregiver_id = user_ids.get("caregiver")
    veterinarian_id = user_ids.get("veterinarian")
    examination_requests = [
        ExaminationRequest(
            caregivers_description="Annual check-up.", id_animal=animal_ids.get("Bella"),
            id_caregiver=caregiver_id, id_veterinarian=veterinarian_id
        ),
        ExaminationRequest(
            caregivers_description="Vaccination needed.", id_animal=animal_ids.get("Mittens"),
            id_caregiver=caregiver_id, id_veterinarian=veterinarian_id
        )
    ]

    db = SessionLocal()
    try:
        db.add_all(examination_requests)
        db.commit()
        print("Example examination requests added to the database.")
    except Exception as e:
        db.rollback()
        print(f"Error adding example examination requests: {e}")
    finally:
        db.close()

def create_example_medical_records(user_ids, animal_ids):
    veterinarian_id = user_ids.get("veterinarian")
    medical_records = [
        MedicalRecord(
            date=date(2021, 7, 21), weight=15.5, vaccination=True, vaccination_type="Rabies",
            vet_description="Healthy and active.", id_animal=animal_ids.get("Bella"), id_veterinarian=veterinarian_id
        ),
        MedicalRecord(
            date=date(2022, 1, 10), weight=8.2, vaccination=True, vaccination_type="Feline distemper",
            vet_description="Good health, recently vaccinated.", id_animal=animal_ids.get("Mittens"), id_veterinarian=veterinarian_id
        )
    ]

    db = SessionLocal()
    try:
        db.add_all(medical_records)
        db.commit()
        print("Example medical records added to the database.")
    except Exception as e:
        db.rollback()
        print(f"Error adding example medical records: {e}")
    finally:
        db.close()

def create_example_animal_borrows(animal_ids):
    borrows = [
        AnimalBorrow(
            date=date(2024, 11, 3), time=time(10, 0), borrowed=True, returned=False,
            id_animal=animal_ids.get("Bella")
        ),
        AnimalBorrow(
            date=date(2024, 11, 2), time=time(10, 0), borrowed=False, returned=False,
            id_animal=animal_ids.get("Bella")
        ),
        AnimalBorrow(
            date=date(2024, 11, 2), time=time(11, 0), borrowed=False, returned=False,
            id_animal=animal_ids.get("Bella")
        ),
        AnimalBorrow(
            date=date(2024, 11, 2), time=time(12, 0), borrowed=False, returned=False,
            id_animal=animal_ids.get("Bella")
        ),
        AnimalBorrow(
            date=date(2022, 8, 16), time=time(14, 30), borrowed=False, returned=False,
            id_animal=animal_ids.get("Mittens")
        )
    ]

    db = SessionLocal()
    try:
        db.add_all(borrows)
        db.commit()
        print("Example animal borrows added to the database.")

        # Return mapping of borrow IDs to animal names
        return {borrow.id: borrow.id_animal for borrow in db.query(AnimalBorrow).all()}
    except Exception as e:
        db.rollback()
        print(f"Error adding example animal borrows: {e}")
    finally:
        db.close()

def create_example_reservations(user_ids, borrow_ids):
    volunteer_id = user_ids.get("volunteer")
    reservations = [
        Reservation(
            approved=True, id_borrow=borrow_ids.get(1), id_volunteer=volunteer_id  # For "Bella"
        ),
        Reservation(
            approved=False, id_borrow=borrow_ids.get(2), id_volunteer=volunteer_id  # For "Mittens"
        )
    ]

    db = SessionLocal()
    try:
        db.add_all(reservations)
        db.commit()
        print("Example reservations added to the database.")
    except Exception as e:
        db.rollback()
        print(f"Error adding example reservations: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    user_ids = create_example_users()
    animal_ids = create_example_animals(user_ids)
    create_example_examination_requests(user_ids, animal_ids)
    create_example_medical_records(user_ids, animal_ids)
    borrow_ids = create_example_animal_borrows(animal_ids)
    create_example_reservations(user_ids, borrow_ids)

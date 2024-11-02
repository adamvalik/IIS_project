from datetime import date
from db import SessionLocal
from models import Animal, User
import os

IMAGE_DIRECTORY = "./images"

def load_image_as_binary(image_name):
    """Reads an image file from the specified directory and returns binary data"""
    file_path = os.path.join(IMAGE_DIRECTORY, image_name)
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

def create_example_animals(user_ids):
    caregiver_id = user_ids.get("caregiver")

    example_animals = [
        Animal(
            name="Bella",
            species="Dog",
            breed="Labrador Retriever",
            birth_year=2018,
            photo=load_image_as_binary("puppy.jpg"),
            admission_date=date(2021, 5, 10),
            size="large",
            caregivers_description="Friendly and outgoing.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Max",
            species="Cat",
            breed="Siamese",
            birth_year=2017,
            photo=load_image_as_binary("kotatko.jpg"),
            admission_date=date(2022, 2, 3),
            size="medium",
            caregivers_description="Curious and playful.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Charlie",
            species="Dog",
            breed="Beagle",
            birth_year=2016,
            photo=load_image_as_binary("puppy.jpg"),
            admission_date=date(2020, 11, 5),
            size="medium",
            caregivers_description="Loyal and affectionate.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Luna",
            species="Rabbit",
            breed="Lionhead",
            birth_year=2019,
            photo=load_image_as_binary("rabbit.jpg"),
            admission_date=date(2021, 6, 15),
            size="small",
            caregivers_description="Gentle and friendly.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Rocky",
            species="Dog",
            breed="German Shepherd",
            birth_year=2015,
            photo=load_image_as_binary("satek.jpg"),
            admission_date=date(2019, 3, 14),
            size="large",
            caregivers_description="Brave and intelligent.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Daisy",
            species="Rabbit",
            breed="Dwarf Hotot",
            birth_year=2020,
            photo=load_image_as_binary("default.png"),
            admission_date=date(2022, 7, 19),
            size="small",
            caregivers_description="Quiet and gentle.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Oliver",
            species="Cat",
            breed="British Shorthair",
            birth_year=2019,
            photo=load_image_as_binary("kotatko.jpg"),
            admission_date=date(2022, 1, 17),
            size="medium",
            caregivers_description="Calm and affectionate.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Coco",
            species="Dog",
            breed="Chihuahua",
            birth_year=2021,
            photo=load_image_as_binary("puppy.jpg"),
            admission_date=date(2023, 3, 10),
            size="small",
            caregivers_description="Lively and bold.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Simba",
            species="Cat",
            breed="Maine Coon",
            birth_year=2017,
            photo=load_image_as_binary("rabbit.jpg"),
            admission_date=date(2021, 9, 22),
            size="large",
            caregivers_description="Gentle and friendly.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Buddy",
            species="Dog",
            breed="Golden Retriever",
            birth_year=2015,
            photo=load_image_as_binary("satek.jpg"),
            admission_date=date(2019, 8, 30),
            size="large",
            caregivers_description="Friendly and loyal.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Milo",
            species="Dog",
            breed="Poodle",
            birth_year=2018,
            photo=load_image_as_binary("puppy.jpg"),
            admission_date=date(2020, 12, 5),
            size="medium",
            caregivers_description="Intelligent and active.",
            id_caregiver=caregiver_id
        ),
        Animal(
            name="Whiskers",
            species="Cat",
            breed="Persian",
            birth_year=2016,
            photo=load_image_as_binary("kotatko.jpg"),
            admission_date=date(2019, 4, 25),
            size="medium",
            caregivers_description="Quiet and gentle.",
            id_caregiver=caregiver_id
        )
    ]

    db = SessionLocal()
    try:
        db.add_all(example_animals)
        db.commit()
        print("Example animals successfully added to the database!")
    except Exception as e:
        db.rollback()
        print(f"Error adding example animals: {e}")
    finally:
        db.close()


def create_example_users():
    users = [
        User(
            email="caregiver@example.com",
            password="satek123",
            name="Bob",
            surname="Caregiver",
            phone_num="987-654-3210",
            role="caregiver",
            verified=None,
            id_caregiver=None
        ),
        User(
            email="vet@example.com",
            password="satek123",
            name="Dr. Smith",
            surname="Veterinarian",
            phone_num="555-555-5555",
            role="veterinarian",
            verified=None,
            id_caregiver=None
        ),
         User(
            email="volunteer@example.com",
            password="satek123",
            name="Alice",
            surname="Volunteer",
            phone_num="123-456-7890",
            role="volunteer",
            verified=False,
            id_caregiver=None
        )
    ]

    db = SessionLocal()
    try:
        db.add_all(users)
        db.commit()
        print("Example users successfully added to the database!")

        return {user.role: user.id for user in db.query(User).all()}

    except Exception as e:
        db.rollback()
        print(f"Error adding example users: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    user_ids = create_example_users()
    create_example_animals(user_ids)

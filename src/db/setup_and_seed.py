from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from src.models import User, Itinerary, ItineraryMember, ItineraryLocation
import json
import pymysql
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, exceptions
import bcrypt


ENV = os.getenv("FASTAPI_ENV", "development")

if ENV == "development":
    load_dotenv(".env.development")
    load_dotenv(".env.firebase")



firebase_cred_info = {
    "type": os.getenv("firebase_type"), 
    "project_id": os.getenv("firebase_project_id"),
    "private_key_id": os.getenv("firebase_private_key_id"),
    "private_key": os.getenv("firebase_private_key").replace('\\n', '\n'),
    "client_email": os.getenv("firebase_client_email"),
    "client_id": os.getenv("firebase_client_id"),
    "auth_uri": os.getenv("firebase_auth_uri"),
    "token_uri": os.getenv("firebase_token_uri"),
    "auth_provider_x509_cert_url": os.getenv("firebase_auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.getenv("firebase_client_x509_cert_url"),
    "universe_domain": os.getenv("firebase_universe_domain"),
}

cred = credentials.Certificate(firebase_cred_info)
firebase_admin.initialize_app(cred)






# the production URL is given and loaded directly by railway

# Function to create the database if it doesn't exist

def create_database():
    connection = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT')),
    )
    with connection.cursor() as cursor:
        name=os.getenv('DB_NAME')
        cursor.execute(f"DROP DATABASE IF EXISTS {name};")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name};")
    connection.close()


# Seed the database with initial data
def seed_data(db: Session):
    # Load data from JSON files
    with open('src/db/data/users.json') as file:
        users = json.load(file)

    with open('src/db/data/itinerary_members.json') as file:
        itinerary_members = json.load(file)

    with open('src/db/data/itineraries.json') as file:
        itineraries = json.load(file)

    with open('src/db/data/itinerary_locations.json') as file:
        itinerary_locations = json.load(file)

    # Add data to the session
    for user in users:
        db.add(User(**user))
    db.commit()
    
    for itinerary in itineraries:
        db.add(Itinerary(**itinerary))
    db.commit()

    for itinerary_member in itinerary_members:
        db.add(ItineraryMember(**itinerary_member))
    db.commit()

    for itinerary_location in itinerary_locations:
        db.add(ItineraryLocation(**itinerary_location))
    db.commit()


# Explanation of this found in firebase docs
# basically retrieves users in batches
def delete_all_users():
    for user in auth.list_users().iterate_all():
        print('User: ' + user.uid)
        auth.delete_user(user.uid)
        print(f'Deleted user: {user.uid}')\
        


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt


def import_seed_users():
    hashed_password, salt = hash_password("password")

    users = [
        auth.ImportUserRecord(
            uid='uPfbGKlVTGTMApk1eKIr4WYPOdh2',
            email='demo@example.com',
            password_hash=hashed_password,
            password_salt=salt
        ),
        auth.ImportUserRecord(
            uid='BWpMeIdDrqfF06Keg90aCVvBut82',
            email='jane@example.com',
            password_hash=hashed_password,
            password_salt=salt
        ),
    ]
    hash_alg = auth.UserImportHash.bcrypt()
    try:
        result = auth.import_users(users, hash_alg=hash_alg)
        for err in result.errors:
            print('Failed to import user:', err.reason)
    except exceptions.FirebaseError as error:
        print('Error importing users:', error)


# If this script is run directly, seed the database
if __name__ == "__main__":
    # Step 1: Create the database
    if ENV == "development":
        create_database()
    else:
        Base.metadata.drop_all(bind=engine)
    
    delete_all_users()
    import_seed_users()

    # Step 2: Setup the database tables before seeding
    Base.metadata.create_all(bind=engine)


    db = SessionLocal()
    try:
        seed_data(db)
        print("Database seeded successfully.")
    finally:
        db.close()
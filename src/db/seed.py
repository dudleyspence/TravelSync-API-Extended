from sqlalchemy.orm import Session
from src.db import engine, Base, SessionLocal
from src.models.SQLAlchemy_Models import User, Group, Itinerary, GroupMember, ItineraryEvent
import json

# Seed the database with initial data
def seed_data(db: Session):
    # Load data from JSON files
    with open('src/db/data/development-data/users.json') as file:
        users = json.load(file)

    with open('src/db/data/development-data/groups.json') as file:
        groups = json.load(file)

    with open('src/db/data/development-data/group_members.json') as file:
        group_members = json.load(file)

    with open('src/db/data/development-data/itineraries.json') as file:
        itineraries = json.load(file)

    with open('src/db/data/development-data/itinerary_events.json') as file:
        itinerary_events = json.load(file)

    # Add data to the session
    for user in users:
        db.add(User(**user))
    db.commit()

    for group in groups:
        db.add(Group(**group))
    db.commit()

    for group_member in group_members:
        db.add(GroupMember(**group_member))
    db.commit()

    for itinerary in itineraries:
        db.add(Itinerary(**itinerary))
    db.commit()

    for itinerary_event in itinerary_events:
        db.add(ItineraryEvent(**itinerary_event))
    db.commit()


# If this script is run directly, seed the database
if __name__ == "__main__":
    # Setup the database before seeding
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_data(db)
        print("Database seeded successfully.")
    finally:
        db.close()

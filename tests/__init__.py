import os
from dotenv import load_dotenv
from src.db import Base, engine, SessionLocal
from src.db.seed import  seed_data

# Set the environment to 'test'
os.environ['FASTAPI_ENV'] = 'test'
load_dotenv(".env.test")

def setup_test_db():
    # Drop and recreate the tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Seed the test database
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

# Run the setup when the test module is imported
setup_test_db()
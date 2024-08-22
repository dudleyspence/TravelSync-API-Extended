from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Determine environment and load the appropriate .env file
ENV = os.getenv('FASTAPI_ENV', 'development')

if ENV == 'development':
    load_dotenv(".env.development")
elif ENV == 'test':
    load_dotenv(".env.test")
else:
    load_dotenv(".env.production")


# Database URL based on the environment
if ENV == 'development':
    DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
elif ENV == 'test':
    DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME_TEST')}"
else:
    DATABASE_URL = os.getenv('DATABASE_URL')

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
ENV = os.getenv('FASTAPI_ENV', 'development')

if ENV == 'development':
    load_dotenv(".env.development")
elif ENV == 'test':
    load_dotenv(".env.test")
else:
    load_dotenv(".env.production")

root_engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
)

def setup_databases():
    with root_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {os.getenv('DB_NAME')};"))
        conn.execute(text(f"DROP DATABASE IF EXISTS {os.getenv('DB_NAME_TEST')};"))
        conn.execute(text(f"CREATE DATABASE {os.getenv('DB_NAME')};"))
        conn.execute(text(f"CREATE DATABASE {os.getenv('DB_NAME_TEST')};"))

if __name__ == "__main__":
    setup_databases()
    print("Databases created successfully.")

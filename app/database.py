import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# fallback (optional safety)
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:postgres@db:5432/bookingdb"

# Retry logic (important for container startup timing)
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        print("Database connected successfully")
        break
    except Exception:
        print("Database not ready, retrying...")
        time.sleep(2)
else:
    raise RuntimeError("Failed to connect to database after retrying")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

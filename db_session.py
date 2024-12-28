from db_postgres.session import SessionLocal
from typing import Generator
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
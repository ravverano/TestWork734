from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
# options
engine_options = {
    "echo": False,
    "pool_pre_ping": True,
    "pool_recycle": 120,
    "pool_size": 10,
    "max_overflow": 20,
}
session_options = {"autocommit": False, "autoflush": False}

# postgres database
engine = create_engine(url=settings.SQLALCHEMY_DATABASE_URI, **engine_options)
SessionLocal = sessionmaker(bind=engine, **session_options)
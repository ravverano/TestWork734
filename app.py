from fastapi import FastAPI, HTTPException
import uvicorn
import os
import logging
from db_postgres.session import engine
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

from api import (
    transactions
)

#  include the modules here
app.include_router(transactions.api_router)

@app.on_event("startup")
async def startup_event():
    # Try to create a database session and execute a test query
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection successful")

         # Automatically create tables for all models
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        logger.error("Database connection failed: %s", e)
        raise RuntimeError(
            "Database connection failed. Application will not start."
        )

@app.get("/")
async def root():
    return {"message": "Hello World"}

port = int(os.getenv("PORT", 5080))
if __name__ == "__main__":
    uvicorn.run(app, port=port, host="0.0.0.0")

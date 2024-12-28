import redis
import celery
import heapq
import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Transactions, Statistics
from db_postgres.session import engine
from sqlalchemy.orm import sessionmaker
from db_session import get_db
# Redis setup for caching statistics
r = redis.Redis(host='localhost', port=6379, db=0)

# Celery setup
celery_app = celery.Celery(
    'worker',
    broker='redis://localhost:6379/0'
)

SessionLocal = sessionmaker(bind=engine)

@celery_app.task
def update_statistics_task():
    from api.transactions.controller import Transaction
    db = SessionLocal()
    try:
        statistics = Transaction.calculate_statistics(db)
        total_transactions = statistics["total_transactions"]
        average_transaction_amount = statistics["average_transaction_amount"]
        top_transactions = statistics["top_transactions"]

        # Update Redis cache
        r.set("transaction_statistics", json.dumps(statistics))

        # Create or update statistics in the database
        stats = db.query(Statistics).first()
        if stats:
            # Update the statistics record
            stats.total_transactions = total_transactions
            stats.average_transaction_amount = average_transaction_amount
            stats.top_transactions = top_transactions
            stats.last_updated = func.now()
        else:
            # If no statistics record exists, create one
            stats = Statistics(
                total_transactions=total_transactions,
                average_transaction_amount=average_transaction_amount,
                top_transactions=top_transactions,
                last_updated=func.now()
            )
            db.add(stats)
            
        # Commit the changes
        db.commit()
    finally:
        db.close()
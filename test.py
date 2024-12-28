from fastapi.testclient import TestClient
from app import app  # Your FastAPI app instance
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_postgres.session import engine
from models import Transactions
from config import settings


# Create tables for testing
SessionLocal = sessionmaker(bind=engine)

client = TestClient(app)

def test_post_transaction():
    # Example input data
    transaction_data = {
        "transaction_id": "123456",
        "user_id": "user_001",
        "amount": 150.50,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }

    response = client.post(
        "/transactions",
        json=transaction_data,
        headers={"Authorization": f"ApiKey {settings.API_KEY}"},
    )

    assert response.status_code == 200

    # Verify transaction was inserted into the database
    db = SessionLocal()
    transaction = (
        db.query(Transactions)
        .filter(Transactions.transaction_id == "123456")
        .first()
    )
    assert transaction is not None
    assert transaction.user_id == "user_001"
    assert transaction.amount == 150.50
    assert transaction.currency == "USD"

def test_delete_transactions():
    # Insert some transactions for testing
    transaction_data = {
        "transaction_id": "123457",
        "user_id": "user_001",
        "amount": 150.50,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }
    client.post(
        "/transactions",
        json=transaction_data,
        headers={"Authorization": f"ApiKey {settings.API_KEY}"}
    )

    # Delete all transactions
    response = client.delete(
        "/transactions",
        headers={"Authorization": f"ApiKey {settings.API_KEY}"}
    )

    assert response.status_code == 200

    # Verify that transactions have been deleted from the database
    db = SessionLocal()
    transactions = db.query(Transactions).all()
    assert len(transactions) == 0


def test_get_statistics():
    # Insert some transactions for testing
    transaction_data1 = {
        "transaction_id": "1",
        "user_id": "user_001",
        "amount": 500.00,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }
    transaction_data2 = {
        "transaction_id": "2",
        "user_id": "user_002",
        "amount": 850.00,
        "currency": "USD",
        "timestamp": "2024-12-13T12:00:00"
    }
    transaction_data3 = {
        "transaction_id": "3",
        "user_id": "user_003",
        "amount": 1000.00,
        "currency": "USD",
        "timestamp": "2024-12-14T12:00:00"
    }
    client.post(
        "/transactions",
        json=transaction_data1,
        headers={"Authorization": f"ApiKey {settings.API_KEY}"}
    )
    client.post(
        "/transactions",
        json=transaction_data2,
        headers={"Authorization": f"ApiKey {settings.API_KEY}"}
    )
    client.post(
        "/transactions",
        json=transaction_data3,
        headers={"Authorization": f"ApiKey {settings.API_KEY}"}
    )

    response = client.get(
        "/statistics",
        headers={"Authorization": f"ApiKey {settings.API_KEY}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_transactions"] == 3
    assert data["average_transaction_amount"] == 783.33  # Expected average
    assert len(data["top_transactions"]) == 3
    assert data["top_transactions"][0]["transaction_id"] == "3"
    assert data["top_transactions"][1]["transaction_id"] == "2"
    assert data["top_transactions"][2]["transaction_id"] == "1"
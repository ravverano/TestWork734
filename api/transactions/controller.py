from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Transactions, Statistics
from workers import celery_worker
from fastapi.encoders import jsonable_encoder
from schemas.response import GetResponse
from fastapi import HTTPException
from library.utils import utils
import heapq, json

class Transaction():

    def __init__(self):
        self.redis = celery_worker.r

    def get_statistics(
        self,
        db: Session
    ):
        
        result = self.redis.get("transaction_statistics")
        if result:
            result = json.loads(result)
        else:
            result = utils.calculate_statistics(db)
            self.redis.set("transaction_statistics", json.dumps(result))

        return result
        
    def create_transaction(
        self,
        db: Session,
        transaction_data: dict
    ):
        # CHECK IF TRANSACTION EXISTS
        existing_transaction = (
            db.query(Transactions)
            .filter_by(transaction_id=transaction_data["transaction_id"])
            .first()
        )

        if existing_transaction:
            return {
                "message": "Transaction ID already exists.",
            }

        # CREATE TRANSACTION
        transaction = Transactions(**transaction_data)
        db.add(transaction)
        db.commit()

        # Send task to reset statistics
        task = celery_worker
        task_result = task.update_statistics_task.apply_async()
        return {
            "message": "Transaction received",
            "task_id": task_result.id
        }
    
    def remove_all_transactions(
        self,
        db: Session
    ):
        try:
            # DELETE ALL TRANSACTIONS
            deleted_count = db.query(Transactions).delete()
            db.commit()

            # DELETE REDIS CACHE
            self.redis.delete("transaction_statistics")

            return {
                "message": f"{deleted_count} Transactions successfully deleted"
            }
        except Exception as e:
            db.rollback()
            return {"message": f"Error: {str(e)}"}
        
    def calculate_statistics(
        self,
        db: Session
    ):
        total_transactions = db.query(
            func.count(Transactions.transaction_id)
        ).scalar() or 0

        # 2. Calculate the average transaction amount
        average_transaction_amount = db.query(
            func.avg(Transactions.amount)
        ).scalar()
        average_transaction_amount = round(average_transaction_amount or 0, 2)

        # 3. Get the top 3 transactions using a heap algorithm
        top_transactions = []
        for transaction in db.query(Transactions).yield_per(1000):
            # Push transaction amounts and IDs into a min-heap with a size of 3
            heapq.heappush(
                top_transactions,
                (float(transaction.amount), transaction.transaction_id)
            )

            # Remove the smallest if there are more than 3
            if len(top_transactions) > 3:
                heapq.heappop(top_transactions)

        # Sort the top transactions in descending order based on amount
        top_transactions = [
            {"transaction_id": t[1], "amount": t[0]} for t in
            sorted(top_transactions, reverse=True)
        ]

        # Format the result into the required JSON structure
        statistics  = {
            "total_transactions": float(total_transactions),
            "average_transaction_amount": float(average_transaction_amount),
            "top_transactions": top_transactions
        }
    
        total_transactions = statistics["total_transactions"]
        average_transaction_amount = statistics["average_transaction_amount"]
        top_transactions = statistics["top_transactions"]
        
transactions = Transaction()

        
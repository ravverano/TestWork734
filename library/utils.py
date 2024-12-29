from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Transactions, Statistics
from workers import celery_worker
from fastapi.encoders import jsonable_encoder
from schemas.response import GetResponse
from fastapi import HTTPException
import heapq, json


class Utils():
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
    
        return statistics

utils = Utils()
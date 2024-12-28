from sqlalchemy import Column, Integer, Float, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    total_transactions = Column(Integer, default=0)
    average_transaction_amount = Column(Float, default=0.0)
    top_transactions = Column(JSON, default=[])
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

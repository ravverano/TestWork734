from sqlalchemy import (
    Column,
    DateTime,
    Text,
    Numeric
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transactions(Base):
    __tablename__  = "transactions"
    transaction_id = Column(Text, primary_key=True)
    user_id = Column(Text, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(Text, nullable=False)
    timestamp = Column(DateTime)


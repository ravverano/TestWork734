
from fastapi import APIRouter, Depends, Request, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_session import get_db
from .controller import transactions as controller
from .schema import (
    CreateTransaction
)
from core.security import validate_api_key

router = APIRouter()

@router.post("/transactions")
async def create_transaction(
    *,
    db: Session = Depends(get_db),
    _: str = Depends(validate_api_key),
    transaction_data: CreateTransaction = Body()
):
    return controller.create_transaction(db, jsonable_encoder(transaction_data))

@router.get("/statistics")
async def get_transactions(
    *,
    db: Session = Depends(get_db),
    _: str = Depends(validate_api_key),
):
    return controller.get_statistics(db)

@router.delete("/transactions")
async def remove_all_transactions(
    *,
    db: Session = Depends(get_db),
    _: str = Depends(validate_api_key),
):
    return controller.remove_all_transactions(db)





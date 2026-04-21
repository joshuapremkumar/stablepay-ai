from fastapi import APIRouter
from database.db import transactions_db

router = APIRouter()

@router.get("/")
def get_transactions():
    return [
        {
            "sender": t.sender,
            "receiver": t.receiver,
            "amount": t.amount,
            "risk_score": t.risk_score,
            "timestamp": t.timestamp
        }
        for t in transactions_db
    ]
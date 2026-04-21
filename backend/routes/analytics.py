from fastapi import APIRouter
from database.db import transactions_db
from services.ai import generate_insights

router = APIRouter()

@router.get("/")
def analytics():
    return generate_insights(transactions_db)
from fastapi import APIRouter, HTTPException
from schemas.payment import PaymentRequest
from services.wallet import transfer
from services.blockchain import send_to_blockchain
from services.ai import fraud_detection
from models.transaction import Transaction
from database.db import transactions_db

router = APIRouter()

@router.post("/")
def make_payment(payment: PaymentRequest):
    success = transfer(payment.sender, payment.receiver, payment.amount)

    if not success:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    blockchain_tx = send_to_blockchain(
        payment.sender, payment.receiver, payment.amount
    )

    risk_score = fraud_detection(payment.amount)

    txn = Transaction(
        payment.sender,
        payment.receiver,
        payment.amount,
        risk_score
    )

    transactions_db.append(txn)

    return {
        "message": "Payment successful",
        "tx_hash": blockchain_tx["tx_hash"],
        "risk_score": risk_score
    }
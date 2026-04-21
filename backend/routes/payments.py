from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

from backend.database import get_db, TransactionDB
from backend.services.blockchain import send_payment
from backend.services.fraud_detection import analyze_transaction

router = APIRouter()


class PaymentRequest(BaseModel):
    amount: str = Field(..., min_length=1)
    recipient: str = Field(..., min_length=1)
    memo: Optional[str] = None
    sender: Optional[str] = '0x742d35Cc6634C0532925a3b844Bc9e7595f4f1E2'


class PaymentResponse(BaseModel):
    success: bool
    txHash: str
    transactionId: str
    amount: str
    recipient: str
    status: str


@router.post('/', response_model=PaymentResponse)
async def create_payment(
    payment: PaymentRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        amount_float = float(payment.amount)
        if amount_float <= 0:
            raise ValueError('Amount must be positive')
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    fraud_result = await analyze_transaction(
        sender=payment.sender,
        recipient=payment.recipient,
        amount=amount_float
    )
    
    if fraud_result['isFlagged']:
        tx_hash = f'0x{"".join(["0" for _ in range(64)])}'
        transaction_id = f'tx_{uuid.uuid4().hex[:8]}'
        
        tx = TransactionDB(
            id=transaction_id,
            from_address=payment.sender,
            to_address=payment.recipient,
            amount=amount_float,
            currency='MATIC',
            type='sent',
            status='flagged',
            timestamp=datetime.utcnow(),
            tx_hash=tx_hash,
            fraud_score=fraud_result['riskScore']
        )
        db.add(tx)
        await db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                'message': 'Transaction flagged by fraud detection',
                'riskScore': fraud_result['riskScore'],
                'reasons': fraud_result.get('reasons', [])
            }
        )
    
    try:
        tx_hash = await send_payment(
            to_address=payment.recipient,
            amount=payment.amount
        )
        
        transaction_id = f'tx_{uuid.uuid4().hex[:8]}'
        
        tx = TransactionDB(
            id=transaction_id,
            from_address=payment.sender,
            to_address=payment.recipient,
            amount=amount_float,
            currency='MATIC',
            type='sent',
            status='completed',
            timestamp=datetime.utcnow(),
            tx_hash=tx_hash,
            fraud_score=fraud_result['riskScore']
        )
        db.add(tx)
        await db.commit()
        
        return PaymentResponse(
            success=True,
            txHash=tx_hash,
            transactionId=transaction_id,
            amount=payment.amount,
            recipient=payment.recipient,
            status='completed'
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Payment failed: {str(e)}'
        )
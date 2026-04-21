from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    from_address: str = Field(..., min_length=42, max_length=66)
    to_address: str = Field(..., min_length=42, max_length=66)
    amount: float = Field(..., gt=0)
    currency: str = Field(default='MATIC')


class TransactionCreate(TransactionBase):
    memo: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: str
    type: str
    status: str
    timestamp: datetime
    tx_hash: Optional[str] = None

    class Config:
        from_attributes = True


class PaymentRequest(BaseModel):
    amount: str = Field(..., min_length=1)
    recipient: str = Field(..., min_length=42)
    memo: Optional[str] = None


class PaymentResponse(BaseModel):
    success: bool
    txHash: str
    transaction_id: str
    amount: str
    recipient: str
    status: str


class WalletBalanceRequest(BaseModel):
    address: str = Field(..., min_length=42, max_length=66)


class WalletBalanceResponse(BaseModel):
    address: str
    balance: str
    currency: str


class AnalyticsRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class FraudCheckRequest(BaseModel):
    amount: float = Field(..., gt=0)
    sender: str = Field(..., min_length=42)
    recipient: str = Field(..., min_length=42)


class FraudCheckResponse(BaseModel):
    risk_score: float
    is_flagged: bool
    reasons: list[str]


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
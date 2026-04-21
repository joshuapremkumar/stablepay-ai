from sqlalchemy import Column, String, Float, Integer, DateTime, Text, Boolean
from backend.database import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(String, primary_key=True)
    from_address = Column(String, nullable=False, index=True)
    to_address = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default='MATIC')
    type = Column(String, nullable=False)
    status = Column(String, default='pending')
    timestamp = Column(DateTime)
    tx_hash = Column(String, unique=True)
    gas_used = Column(String)
    block_number = Column(Integer)
    fraud_score = Column(Float)


class Wallet(Base):
    __tablename__ = 'wallets'
    
    address = Column(String, primary_key=True)
    private_key_encrypted = Column(Text, nullable=False)
    balance = Column(Float, default=0.0)
    is_merchant = Column(Boolean, default=False)
    created_at = Column(DateTime)
    last_synced = Column(DateTime)


__all__ = ['Transaction', 'Wallet']
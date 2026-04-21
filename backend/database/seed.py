from datetime import datetime, timedelta
import random
import json
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.db import TransactionDB, AsyncSession

SAMPLE_ADDRESSES = [
    '0x742d35Cc6634C0532925a3b844Bc9e7595f4f1E2',
    '0x8ba1f109551bD21DD697c5e62d3fB5C5e8f1aB2f',
    '0x1234567890abcdef1234567890abcdef12345678',
    '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
]


async def seed_data():
    async with AsyncSession() as session:
        result = await session.execute("SELECT COUNT(*) FROM transactions")
        count = result.scalar()
        
        if count > 0:
            return
        
        transactions = []
        base_time = datetime.utcnow() - timedelta(days=7)
        
        for i in range(25):
            is_received = random.random() > 0.5
            tx = TransactionDB(
                id=f'tx_{i:04d}',
                from_address=random.choice(SAMPLE_ADDRESSES),
                to_address=random.choice(SAMPLE_ADDRESSES),
                amount=round(random.uniform(0.1, 10.0), 4),
                currency='MATIC',
                type='received' if is_received else 'sent',
                status='completed',
                timestamp=base_time + timedelta(hours=i * 6),
                tx_hash=f'0x{"".join([random.choice("0123456789abcdef") for _ in range(64)])}',
                fraud_score=random.uniform(0, 0.3)
            )
            transactions.append(tx)
        
        session.add_all(transactions)
        await session.commit()


async def seed_analytics():
    async with AsyncSession() as session:
        from backend.database.db import AnalyticsDB
        
        for i in range(7):
            hourly = json.dumps([random.uniform(100, 500) for _ in range(24)])
            daily = json.dumps([random.uniform(1000, 5000) for _ in range(7)])
            
            analytics = AnalyticsDB(
                date=datetime.utcnow() - timedelta(days=i),
                total_volume=random.uniform(2000, 8000),
                total_transactions=random.randint(20, 100),
                fraud_prevented=random.uniform(100, 500),
                peak_hour=random.randint(10, 20),
                hourly_volume=hourly,
                daily_volume=daily
            )
            session.add(analytics)
        
        await session.commit()
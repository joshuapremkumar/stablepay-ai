import logging
from typing import Dict, List
import os

from ai_engine.fraud_detection import FraudDetector

logger = logging.getLogger(__name__)

fraud_detector = FraudDetector()


async def analyze_transaction(
    sender: str,
    recipient: str,
    amount: float
) -> Dict[str, any]:
    try:
        result = fraud_detector.analyze(
            sender_address=sender,
            recipient_address=recipient,
            amount=amount
        )
        
        logger.info(f'Fraud analysis: risk={result["riskScore"]:.2f}, flagged={result["isFlagged"]}')
        return result
        
    except Exception as e:
        logger.error(f'Fraud detection error: {e}')
        return {
            'riskScore': 0.0,
            'isFlagged': False,
            'reasons': ['Analysis unavailable']
        }


async def batch_analyze(
    transactions: List[Dict[str, any]]
) -> List[Dict[str, any]]:
    results = []
    for tx in transactions:
        result = await analyze_transaction(
            sender=tx.get('sender', ''),
            recipient=tx.get('recipient', ''),
            amount=tx.get('amount', 0)
        )
        results.append(result)
    return results
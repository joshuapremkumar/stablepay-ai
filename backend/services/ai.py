def fraud_detection(amount):
    if amount > 500:
        return 80
    return 10


def generate_insights(transactions):
    if not transactions:
        return {"message": "No data"}

    total = sum(t.amount for t in transactions)
    avg = total / len(transactions)

    return {
        "total_transactions": len(transactions),
        "total_volume": total,
        "average_transaction": avg
    }
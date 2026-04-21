from datetime import datetime

class Transaction:
    def __init__(self, sender, receiver, amount, risk_score):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.risk_score = risk_score
        self.timestamp = datetime.utcnow()
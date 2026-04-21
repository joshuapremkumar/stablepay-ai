from pydantic import BaseModel

class PaymentRequest(BaseModel):
    sender: str
    receiver: str
    amount: float
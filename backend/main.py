from fastapi import FastAPI
from routes import payment, transactions, analytics

app = FastAPI(title="StablePay AI Backend")

app.include_router(payment.router, prefix="/pay", tags=["Payments"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {"message": "StablePay AI Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
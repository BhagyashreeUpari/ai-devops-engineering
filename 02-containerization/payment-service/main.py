from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI(title="Payment Service", version="1.0.0")


class PaymentRequest(BaseModel):
    amount: float
    currency: str = "USD"


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "payment-service",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/payment")
def process_payment(payment: PaymentRequest):
    payment_id = str(uuid.uuid4())

    return {
        "payment_id": payment_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "status": "SUCCESS",
        "version": "1.1.0",
        "service": "payment-service"
    }
# StablePay AI API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check

#### GET /

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "StablePay AI",
  "version": "1.0.0"
}
```

#### GET /health

Detailed health check.

**Response:**
```json
{
  "status": "ok",
  "database": "connected",
  "blockchain": "ready"
}
```

---

## Transactions

### GET /transactions

List all transactions with pagination.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | int | 50 | Max results |
| offset | int | 0 | Skip results |
| status_filter | string | - | Filter by status |

**Response:**
```json
{
  "transactions": [
    {
      "id": "tx_0001",
      "from": "0x742d35Cc6634...",
      "to": "0x8ba1f109551...",
      "amount": 1.5,
      "currency": "MATIC",
      "type": "sent",
      "status": "completed",
      "timestamp": "2024-01-15T10:30:00Z",
      "txHash": "0xabc123..."
    }
  ],
  "total": 25
}
```

### GET /transactions/{tx_id}

Get transaction details by ID.

**Response:**
```json
{
  "id": "tx_0001",
  "from": "0x742d35Cc6634...",
  "to": "0x8ba1f109551...",
  "amount": 1.5,
  "currency": "MATIC",
  "type": "sent",
  "status": "completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "txHash": "0xabc123..."
}
```

---

## Payments

### POST /pay

Create a new payment.

**Request:**
```json
{
  "amount": "0.5",
  "recipient": "0x8ba1f109551bD21DD697c5e62d3fB5C5e8f1aB2f",
  "memo": "Payment for services"
}
```

**Response:**
```json
{
  "success": true,
  "txHash": "0xdef456...",
  "transactionId": "tx_0002",
  "amount": "0.5",
  "recipient": "0x8ba1f109551bD21DD697c5e62d3fB5C5e8f1aB2f",
  "status": "completed"
}
```

**Error Response (Fraud Flagged):**
```json
{
  "detail": {
    "message": "Transaction flagged by fraud detection",
    "riskScore": 0.85,
    "reasons": ["Unusual transaction pattern detected"]
  }
}
```

---

## Analytics

### GET /analytics

Get analytics overview.

**Response:**
```json
{
  "totalVolume": 15000.50,
  "averageTransaction": 250.00,
  "peakHour": 14,
  "fraudPrevented": 2500.00,
  "totalTransactions": 60,
  "hourlyVolume": [100, 150, 200, ...],
  "dailyVolume": [2000, 2500, 3000, ...]
}
```

### POST /analytics/fraud-check

Check fraud risk for a transaction.

**Request:**
```json
{
  "amount": 500.0,
  "sender": "0x742d35Cc6634...",
  "recipient": "0x8ba1f109551..."
}
```

**Response:**
```json
{
  "riskScore": 0.15,
  "isFlagged": false,
  "reasons": []
}
```

---

## Wallet

### GET /wallet/{address}/balance

Get wallet balance.

**Response:**
```json
{
  "address": "0x742d35Cc6634...",
  "balance": "2.5",
  "currency": "MATIC"
}
```

### POST /wallet/generate

Generate new wallet.

**Response:**
```json
{
  "address": "0xabc123...",
  "private_key": "0xprivatekey..."
}
```

---

## Error Responses

All endpoints may return:

### 400 Bad Request
```json
{
  "detail": "Invalid amount"
}
```

### 404 Not Found
```json
{
  "detail": "Transaction not found"
}
```

### 403 Forbidden
```json
{
  "detail": {
    "message": "Transaction flagged by fraud detection",
    "riskScore": 0.85,
    "reasons": ["Amount exceeds limit"]
  }
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error": "Error message"
}
```

---

## Rate Limits

- API requests: 100/minute per IP
- Payments: 10/minute per wallet
- Fraud checks: 50/minute

---

## WebSocket (Future)

Real-time transaction updates will be available via WebSocket.

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('New transaction:', data);
};
```
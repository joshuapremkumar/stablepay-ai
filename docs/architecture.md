# StablePay AI Architecture

## System Overview

StablePay AI is a full-stack AI-powered payment platform that combines blockchain technology with machine learning for fraud detection and analytics.

## Architecture Layers

```
┌─────────────────────────────────────────────────┐
│                  Frontend (Next.js)             │
│  - Dashboard / Payments UI / Analytics           │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│                 Backend (FastAPI)                │
│  - REST API / Authentication / Database          │
└─────────────────────┬───────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│ AI Engine     │           │  Blockchain   │
│ Fraud Detect  │           │  (Polygon)    │
│ Analytics     │           │  Smart Contract│
└───────────────┘           └───────────────┘
```

## Frontend (Next.js)

### Technologies
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React hooks + Context
- **Blockchain**: ethers.js
- **Charts**: Recharts

### Directory Structure
```
frontend/
├── pages/              # Next.js pages
│   ├── _app.tsx       # App entry
│   ├── _document.tsx  # HTML document
│   └── index.tsx      # Dashboard
├── components/         # React components
│   ├── PaymentModal.tsx
│   ├── TransactionList.tsx
│   └── AnalyticsChart.tsx
├── services/          # API integration
│   └── api.ts
├── styles/           # CSS
│   └── globals.css
└── utils/            # Types & helpers
    └── types.ts
```

## Backend (FastAPI)

### Technologies
- **Framework**: FastAPI
- **Database**: SQLite (async) / PostgreSQL
- **ORM**: SQLAlchemy
- **Blockchain**: web3.py

### API Endpoints

#### Transactions
- `GET /transactions` - List all transactions
- `GET /transactions/{id}` - Get transaction details

#### Payments
- `POST /pay` - Create payment

#### Analytics
- `GET /analytics` - Get analytics data
- `POST /analytics/fraud-check` - Check fraud risk

#### Wallet
- `GET /wallet/{address}/balance` - Get wallet balance
- `POST /wallet/generate` - Generate new wallet

### Directory Structure
```
backend/
├── main.py           # FastAPI app entry
├── routes/           # API routes
│   ├── transactions.py
│   ├── payments.py
│   ├── analytics.py
│   └── wallet.py
├── services/         # Business logic
│   ├── blockchain.py
│   ├── fraud_detection.py
│   └── wallet.py
├── models/           # DB models
├── schemas/          # Pydantic schemas
└── database/        # DB setup
```

## Blockchain (Polygon)

### Smart Contract: Payment.sol

The Payment contract handles payment processing on the Polygon blockchain.

#### Features
- Send payments to recipients
- Merchant registration
- Payment history tracking
- Reentrancy protection

#### Functions
```
function sendPayment(address payable to, uint256 amount) external payable
function getPaymentDetails(bytes32 paymentId) external view
function registerMerchant(address merchant) external onlyOwner
function getContractBalance() external view
```

## AI Engine

### Fraud Detection

The fraud detection system uses:
1. **Rule-based checks** - Known scam patterns, amount limits
2. **ML Model** - Decision tree classifier for anomaly detection

#### Features
- Transaction risk scoring
- Batch analysis
- Model training capability

### Analytics

The analytics engine provides:
- Peak hour detection
- Volume analysis
- Pattern recognition
- Simple forecasting

## Database Schema

### Transactions Table
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Transaction ID |
| from_address | String | Sender address |
| to_address | String | Recipient address |
| amount | Float | Amount in MATIC |
| type | String | sent/received |
| status | String | pending/completed/flagged |
| timestamp | DateTime | Transaction time |
| tx_hash | String | Blockchain tx hash |
| fraud_score | Float | ML fraud score |

## Deployment

### Environment Variables
```env
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BLOCKCHAIN_RPC=https://rpc-amoy.polygon.technology
NEXT_PUBLIC_CONTRACT_ADDRESS=

# Backend
DATABASE_URL=sqlite+aiosqlite:///./stablepay.db
POLYGON_RPC=https://rpc-amoy.polygon.technology
WALLET_PRIVATE_KEY=

# Blockchain
PRIVATE_KEY=
POLYGON_RPC_URL=
POLYGONSCAN_API_KEY=
```

### Docker Compose

Services:
- `frontend` - Next.js app (port 3000)
- `backend` - FastAPI app (port 8000)

## Security Considerations

1. **Fraud Detection** - All transactions pre-screened by AI
2. **Smart Contract** - Reentrancy guards, access control
3. **API** - Rate limiting, input validation
4. **Database** - Parameterized queries, async operations

## Future Enhancements

- Multi-chain support (ETH, BSC)
- Real ML model training pipeline
- Merchant dashboard with KYC
- Mobile app (React Native)
- Stablecoin integration
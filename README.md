# StablePay AI

<p align="center">
  <img src="https://img.shields.io/badge/StablePay-AI-8b5cf6?style=for-the-badge&logo=blockchain&logoColor=white" alt="StablePay AI">
  <img src="https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=nextdotjs" alt="Next.js">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Polygon-8247e5?style=for-the-badge&logo=polygon" alt="Polygon">
  <img src="https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/TypeScript-3178c6?style=for-the-badge&logo=typescript" alt="TypeScript">
</p>

<p align="center">
  <a href="https://github.com/joshuapremkumar/stablepay-ai/stargazers">
    <img src="https://img.shields.io/github/stars/joshuapremkumar/stablepay-ai?style=social" alt="Stars">
  </a>
  <a href="https://github.com/joshuapremkumar/stablepay-ai/forks">
    <img src="https://img.shields.io/github/forks/joshuapremkumar/stablepay-ai?style=social" alt="Forks">
  </a>
  <a href="https://github.com/joshuapremkumar/stablepay-ai/issues">
    <img src="https://img.shields.io/github/issues/joshuapremkumar/stablepay-ai" alt="Issues">
  </a>
  <img src="https://img.shields.io/github/license/joshuapremkumar/stablepay-ai" alt="License">
</p>

---

> **Smart Stablecoin Payments + Intelligence Layer** — A blockchain-native payment infrastructure that enables merchants to seamlessly accept stablecoin payments while unlocking real-time financial insights through AI.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 💳 **QR Payments** | Scan-to-pay stablecoin transactions |
| ⚡ **Instant Settlement** | Fast blockchain transactions on Polygon |
| 🧠 **AI Fraud Detection** | Machine learning-powered risk analysis |
| 📊 **Analytics Dashboard** | Real-time transaction insights |
| 🔗 **Smart Contracts** | Secure on-chain payment logic |
| 🔒 **Secure Wallet** | Encrypted wallet management |

---

## 🌍 The Problem

Despite rapid growth in digital payments and cryptocurrency adoption, merchants still lack simple, compliant, and scalable tools to accept stablecoin payments in real-world transactions.

- ❌ High transaction fees (2-3%)
- ❌ Delayed settlements
- ❌ No merchant-friendly stablecoin POS systems
- ❌ No intelligence from transaction data

**This creates a gap between consumer capability (crypto adoption) and merchant readiness.**

---

## 💡 The Solution

StablePay AI bridges traditional finance and blockchain by providing:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Customer   │────▶│  Backend    │────▶│  Blockchain │
│  (QR Scan)  │     │  (FastAPI)  │     │  (Polygon)  │
└──────────────┘     └──────────────┘     └──────────────┘
                           │
                    ┌──────┴──────┐
                    │  AI Engine  │
                    │  ( Fraud +  │
                    │  Analytics)│
                    └────────────┘
```

- ✅ QR-based stablecoin payments
- ✅ Instant settlement on blockchain
- ✅ AI-powered fraud detection & insights
- ✅ Merchant dashboard for analytics

---

## 🏗️ Architecture

```
                    ┌─────────────────────┐
                    │   Frontend (Next.js)  │
                    │  • Dashboard        │
                    │  • QR Payments      │
                    │  • Analytics UI    │
                    └──────────┬──────────┘
                               │ REST API
                    ┌──────────▼──────────┐
                    │  Backend (FastAPI)   │
                    │  • REST API         │
                    │  • Fraud Detection │
                    │  • Wallet Logic    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼─────────┐ ┌──▼────┐ ┌─────▼─────┐
    │      AI Engine     │ │Database│ │Blockchain│
    │  • Fraud Detect  │ │SQLite  │ │ Polygon  │
    │  • Analytics   │ │       │ │ Contracts│
    └────────────────┘ └───────┘ └──────────┘
```

---

## 🔄 How It Works

1. **Customer scans QR code** — Mobile wallet initiates payment
2. **Payment request sent to backend** — FastAPI processes transaction
3. **AI analyzes risk** — Fraud detection check
4. **Transaction on blockchain** — Polygon processes payment
5. **Funds settled instantly** — Merchant receives payment
6. **Dashboard updates** — Real-time analytics

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS |
| **Backend** | FastAPI, Python 3.11 |
| **Blockchain** | Solidity, Hardhat, Polygon |
| **AI/ML** | scikit-learn, pandas |
| **Database** | SQLite (async) |

---

## 🚦 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- npm or yarn
- Hardhat (for blockchain)

### 1. Clone the Repository

```bash
git clone https://github.com/joshuapremkumar/stablepay-ai.git
cd stablepay-ai
```

### 2. Run Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 3. Run Frontend

```bash
cd frontend
npm install
npm run dev
# App: http://localhost:3000
```

### 4. Blockchain (Optional)

```bash
cd blockchain
npm install
npx hardhat compile
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|---------|--------|------------|
| `/pay` | POST | Make a payment |
| `/transactions` | GET | List transactions |
| `/analytics` | GET | Get analytics |
| `/health` | GET | Health check |

---

## 🎯 Target Customers

- 🏪 SMEs (retail stores, cafes, restaurants)
- ✈️ Tourist businesses (hotels, malls, airports)
- 🛒 E-commerce merchants
- 🌟 Early adopters of crypto payments

---

## 💰 Business Model

### Revenue Streams
- Transaction fees (0.5%-1%)
- Subscription for analytics dashboard
- Premium AI features

### Cost Structure
- Development & engineering
- Cloud infrastructure
- Blockchain gas costs

---

## 🔮 Future Roadmap

- [ ] Polygon mainnet integration
- [ ] Advanced ML fraud detection model
- [ ] Predictive analytics
- [ ] SME credit scoring
- [ ] Mobile app (React Native)
- [ ] Multi-chain support (ETH, BSC, Avalanche)

---

## 👥 Team

| Role | Name | Focus |
|------|------|-------|
| 🎨 Lead | **Joshua Premkumar** | Product & System Design |
| 🧠 AI | **Ilyes Sais** | AI Research |
| 🔬 ML | **Mohy M** | Machine Learning & Applied Math |

---

## 🤝 Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) first.

```bash
# Fork the repo
# Create your feature branch
git checkout -b feature/amazing-feature
# Commit your changes
git commit -m 'Add amazing feature'
# Push to the branch
git push origin feature/amazing-feature
# Open a Pull Request
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🌟 Show Your Support

Give a ⭐ if this project helped you!

[![GitHub stars](https://img.shields.io/github/stars/joshuapremkumar/stablepay-ai?style=social)](https://github.com/joshuapremkumar/stablepay-ai/stargazers)

---

## 📬 Contact

- 📧 Email: joshuaezekiel334@gmail.com
- 🐦 Twitter: [@joshuapremkumar](https://twitter.com/joshuapremkumar)
- 🔗 LinkedIn: [Joshua Premkumar](https://linkedin.com/in/joshuapremkumar)

---

<p align="center">
  <strong>Vision:</strong> To become the <em>Stripe for stablecoin payments</em>, powered by AI and built for the global digital economy.
</p>

<p align="center">
  Made with ❤️ by the StablePay AI team
</p>
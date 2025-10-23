# DDD Coin Analysis Dashboard

## Project Overview

A comprehensive cryptocurrency analysis dashboard focused on tracking the **DDD Token (Durgan Dynasty Doubloon)** and its trading pairs across decentralized exchanges on Polygon. The project provides real-time price data, historical charts, technical indicators, and portfolio tracking through a multi-source API architecture with intelligent fallback.

---

## 🎯 Project Goals

1. **Track DDD Token**: Monitor price, volume, liquidity, and market metrics
2. **Monitor Trading Pairs**: Track 9+ DDD/TOKEN pairs (USDGLO, axiREGEN, CCC, etc.)
3. **LP Pool Analytics**: Analyze 3 liquidity pool positions
4. **Technical Analysis**: Provide RSI, MACD, Bollinger Bands, and other indicators
5. **Dashboard UI**: Create intuitive, real-time dashboard for portfolio management

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND DASHBOARD                       │
│              (React/Next.js - Port 3000)                    │
│   - Token price cards                                       │
│   - Interactive charts (Chart.js/Recharts)                  │
│   - Technical indicators display                            │
│   - Portfolio value tracker                                 │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST API
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND API (FastAPI)                     │
│                  (Python - Port 8000)                       │
│                                                             │
│   ┌──────────────────────────────────────────────────┐    │
│   │         UnifiedPriceService                      │    │
│   │    (Orchestrates all data sources)               │    │
│   └──────┬─────────────┬──────────────┬──────────────┘    │
│          │             │              │                    │
│   ┌──────▼──────┐ ┌───▼────────┐ ┌──▼──────────┐        │
│   │GeckoTerminal│ │ DeFiLlama  │ │  Alchemy    │        │
│   │  Service    │ │  Service   │ │  Service    │        │
│   └─────────────┘ └────────────┘ └─────────────┘        │
│                                                            │
│   ┌─────────────┐ ┌────────────────────────────┐         │
│   │   Zapper    │ │   PortfolioService         │         │
│   │  Service    │ │  (Aggregates all tokens)   │         │
│   └─────────────┘ └────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              EXTERNAL APIs (All FREE Tier)                  │
│  • GeckoTerminal (DEX data) - 30 calls/min                 │
│  • DeFiLlama (Exotic tokens) - Unlimited                   │
│  • Alchemy (Metadata) - 300M compute units/mo              │
│  • Zapper (Pool stats) - Free tier + credits               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
coin-analysis/
├── api/                          # Backend Python API
│   ├── index.py                  # FastAPI main app with all endpoints
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables (API keys)
│   │
│   ├── Services/
│   ├── geckoterminal_service.py  # GeckoTerminal API client
│   ├── defillama_service.py      # DeFiLlama API client
│   ├── alchemy_service.py        # Alchemy API client
│   ├── zapper_service.py         # Zapper API client [TO CREATE]
│   ├── unified_price_service.py  # Multi-source orchestration
│   ├── portfolio_service.py      # Portfolio aggregation
│   ├── crypto_service.py         # CoinGecko for major cryptos
│   ├── technical_analysis.py     # Technical indicators
│   │
│   ├── Configuration/
│   ├── token_config.py           # DDD token portfolio config
│   │
│   └── Testing/
│       └── test_tokens.py        # Token API testing script
│
├── frontend/                     # Frontend React/Next.js [TO CREATE]
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/            # API client
│   │   ├── hooks/               # Custom React hooks
│   │   └── pages/               # Dashboard pages
│   ├── public/                  # Static assets
│   └── package.json             # Node dependencies
│
├── Documentation/
├── claude.md                    # This file - project overview
├── DASHBOARD_STRATEGY.md        # Complete implementation strategy
├── PRICE_API_IMPLEMENTATION.md  # API documentation
├── TOKEN_TRACKING.md            # Token tracking guide
└── README.md                    # Project README
│
└── vercel.json                  # Vercel deployment config
```

---

## 🔑 Key Components

### **Backend Services**

#### **1. UnifiedPriceService** (`unified_price_service.py`)
- **Purpose**: Orchestrates multiple price data sources with intelligent fallback
- **Priority**: GeckoTerminal → DeFiLlama → Alchemy
- **Methods**:
  - `get_token_price()` - Get price with automatic fallback
  - `get_token_with_historical()` - Price + OHLCV data
  - `compare_sources()` - Debug price discrepancies
  - `health_check()` - Service status monitoring

#### **2. GeckoTerminalService** (`geckoterminal_service.py`)
- **Purpose**: Primary price source for DEX-traded tokens
- **Coverage**: 1,700+ DEXs, 250+ networks
- **Methods**:
  - `get_token_price()` - Current price, volume, liquidity
  - `get_historical_ohlcv()` - Historical candlestick data
  - `search_pools()` - Find trading pools

#### **3. DeFiLlamaService** (`defillama_service.py`)
- **Purpose**: Fallback for exotic/LP tokens
- **Specialty**: On-chain price calculations
- **Methods**:
  - `get_token_price()` - Current price
  - `get_historical_prices()` - Historical data
  - `get_multiple_token_prices()` - Batch requests

#### **4. AlchemyService** (`alchemy_service.py`)
- **Purpose**: Token metadata (no price data)
- **API Key**: Configured in `.env`
- **Methods**:
  - `get_token_metadata()` - Name, symbol, decimals, logo
  - `get_token_balances()` - Wallet balances

#### **5. ZapperService** (`zapper_service.py`) [TO CREATE]
- **Purpose**: LP pool statistics and DeFi positions
- **Methods** (Planned):
  - `get_pool_stats()` - Pool reserves, liquidity
  - `get_token_balances()` - DeFi positions
  - `calculate_pool_price()` - Price from reserves

#### **6. PortfolioService** (`portfolio_service.py`)
- **Purpose**: Aggregate all DDD tokens and pairs
- **Methods**:
  - `get_portfolio_summary()` - Complete portfolio data
  - `get_portfolio_prices_only()` - Quick price updates
  - `get_top_pairs_by_liquidity()` - Best pairs
  - `get_top_pairs_by_volume()` - Most active pairs

#### **7. TechnicalAnalysis** (`technical_analysis.py`)
- **Purpose**: Calculate trading indicators
- **Indicators**:
  - Moving Averages (SMA 20/50/200, EMA 12/26)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Volume trends
  - Overall signal (bullish/bearish/neutral)

---

## 🌐 API Endpoints

### **V2 Unified Endpoints (Recommended)**

```
GET  /v2/token/{contract_address}
     ?network=polygon
     → Get token with automatic fallback

GET  /v2/token/{contract_address}/historical
     ?network=polygon&days=30
     → Token + OHLCV historical data

GET  /v2/token/{contract_address}/indicators
     ?network=polygon&days=30
     → Token + technical indicators

GET  /v2/tokens/batch
     ?contracts=0x...,0x...&networks=polygon,ethereum
     → Multiple tokens at once

GET  /v2/token/{contract_address}/compare
     ?network=polygon
     → Compare prices across all sources (debug)

GET  /v2/health
     → Health check for all services
```

### **Portfolio Endpoints** [TO ADD]

```
GET  /v2/portfolio/summary
     → Complete DDD portfolio data

GET  /v2/portfolio/prices
     → Quick price updates for dashboard

GET  /v2/portfolio/ddd
     → Main DDD token with full details

GET  /v2/portfolio/pairs
     → All DDD trading pairs

GET  /v2/portfolio/pools
     → LP pool positions
```

### **Direct Service Endpoints**

```
GET  /geckoterminal/token/{contract_address}
     → Direct GeckoTerminal query

GET  /geckoterminal/search?query=USDC
     → Search pools

GET  /defillama/token/{contract_address}
     → Direct DeFiLlama query

GET  /crypto/token/alchemy/{contract_address}
     → Direct Alchemy metadata
```

### **Legacy Endpoints (Still Supported)**

```
GET  /crypto/price/{symbol}
     → CoinGecko major crypto prices

GET  /crypto/historical/{symbol}
     → Historical data for major cryptos

GET  /crypto/indicators/{symbol}
     → Technical indicators for major cryptos

GET  /crypto/top?limit=20
     → Top cryptocurrencies by market cap
```

---

## 🪙 Tracked Tokens

### **Main Token**
- **DDD (Durgan Dynasty Doubloon)**
  - Contract: `0x4bf82cf0d6b2afc87367052b793097153c859d38`
  - Network: Polygon
  - Status: ✅ Fully tracked (GeckoTerminal)

### **Quote Tokens (9)**
1. USDGLO - `0x7ee2dd0022e3460177b90b8f8fa3b3a76d970ff6`
2. axiREGEN - `0x520a3b3faca7ddc8dc8cd3380c8475b67f3c7b8d`
3. CCC - `0x73e6a1630486d0874ec56339327993a3e4684691`
4. PR24 - `0xa249cc5719da5457b212d9c5f4b1e95c7f597441`
5. NCT - `0xfc983c854683b562c6e0f858a15b32698b32ba45`
6. JCGWR - `0x7aadf47b49202b904b0f62e533442b09fcaa2614`
7. AU24T - `0xdaa015423b5965f1b198119cd8940e0e551cd74c`
8. JLT-F24 - `0x4faf57a632bd809974358a5fff9ae4aec5a51b7d`
9. JLT-F24 (v2) - `0xf2bda2e42fbd1ec6ee61b9e11aeb690eb88956c1`

**Status**: ⚠️ Not indexed by APIs (will use pool data)

### **LP Pools (3)**
1. DDD/JLT-B23 - `0xac6c98888209c2cccb500e0b1afb70fb2474611b1520d4f55e1968518179f40c`
2. DDD/TB01 - `0x54c0a64be7d50e9a8e6b7de50055982934b3d09bfaedfff6cc1c5190d0ba83d7`
3. DDD/MC02 - `0xebb0ef84907875a6004d89268df1534c6a8dff2441e653c90f1c07f51adcfb8a`

**Status**: ⏳ To implement via Zapper pool stats

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.9+
- **HTTP Client**: aiohttp (async)
- **Deployment**: Vercel Serverless (Mangum adapter)
- **Environment**: python-dotenv

### **Frontend** [TO IMPLEMENT]
- **Framework**: React 18+ or Next.js 14+
- **Build Tool**: Vite or Next.js
- **Charts**: Chart.js or Recharts
- **Styling**: Tailwind CSS or styled-components
- **State Management**: React Context or Zustand
- **HTTP Client**: Axios or Fetch API

### **External APIs**
- GeckoTerminal (Free, 30 req/min)
- DeFiLlama (Free, unlimited)
- Alchemy (Free tier, 300M compute units/mo)
- Zapper (Free tier + credits)
- CoinGecko (Free for major cryptos)

---

## 🔐 Environment Variables

Create `api/.env`:

```bash
# Alchemy API Key (Already configured)
ALCHEMY_API_KEY=iLNESlBkd0XdXg2lfRKg2

# Zapper API Key (To be added)
ZAPPER_API_KEY=your_zapper_key_here

# Optional: Rate limiting config
RATE_LIMIT_CALLS=30
RATE_LIMIT_PERIOD=60
```

---

## 🚀 Development Setup

### **Backend Setup**

```bash
# Navigate to API directory
cd api

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn index:app --reload --port 8000

# Test API
curl http://localhost:8000/v2/health
```

### **Test Tokens**

```bash
# Quick test (DDD only)
python test_tokens.py quick

# Test all tokens
python test_tokens.py
```

### **Frontend Setup** [TO CREATE]

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Access dashboard
open http://localhost:3000
```

---

## 📊 Current Status

### **✅ Completed**
- [x] Multi-source API infrastructure (GeckoTerminal, DeFiLlama, Alchemy)
- [x] Unified price service with intelligent fallback
- [x] Portfolio service for DDD token tracking
- [x] Token configuration management
- [x] Technical indicators engine
- [x] V2 API endpoints
- [x] Alchemy API key configuration
- [x] Comprehensive testing scripts
- [x] Full documentation

### **🔄 In Progress**
- [ ] Zapper API integration for LP pools
- [ ] Portfolio endpoints implementation
- [ ] Pool price calculator

### **📋 To Do**
- [ ] Frontend dashboard UI
- [ ] Chart components
- [ ] Real-time price updates
- [ ] Price alerts system
- [ ] Caching layer
- [ ] WebSocket support (optional)

---

## 🎯 Implementation Priorities

### **Phase 1: Complete Backend** (Current)
1. ✅ Integrate Zapper API for pool data
2. ✅ Add portfolio endpoints to index.py
3. ✅ Create pool price calculator
4. ✅ Test all endpoints thoroughly

### **Phase 2: Frontend Dashboard**
1. Set up React/Next.js project
2. Create layout and navigation
3. Build token price cards
4. Implement chart components
5. Add technical indicators display
6. Connect to backend API

### **Phase 3: Polish & Deploy**
1. Add loading states and error handling
2. Implement responsive design
3. Add dark/light mode
4. Optimize performance
5. Deploy to Vercel
6. Add monitoring and analytics

---

## 📝 Coding Conventions

### **Python (Backend)**
- Follow PEP 8 style guide
- Use type hints for all functions
- Async/await for all I/O operations
- Comprehensive docstrings
- Error handling with try/except
- Logging for debugging

### **JavaScript/TypeScript (Frontend)**
- ES6+ syntax
- Functional components with hooks
- PropTypes or TypeScript for type safety
- Descriptive variable names
- Component composition
- Async/await for API calls

---

## 🧪 Testing

### **Backend Tests**
```bash
# Test individual service
python -c "from geckoterminal_service import GeckoTerminalService; import asyncio; print(asyncio.run(GeckoTerminalService().get_token_price('0x4bf82cf0d6b2afc87367052b793097153c859d38', 'polygon')))"

# Test unified service
curl http://localhost:8000/v2/token/0x4bf82cf0d6b2afc87367052b793097153c859d38?network=polygon

# Health check
curl http://localhost:8000/v2/health
```

### **Frontend Tests** [TO ADD]
```bash
# Unit tests
npm test

# E2E tests
npm run test:e2e
```

---

## 📚 Documentation Files

- `claude.md` - This file (project overview)
- `DASHBOARD_STRATEGY.md` - Implementation strategy
- `PRICE_API_IMPLEMENTATION.md` - API documentation
- `TOKEN_TRACKING.md` - Token tracking guide
- `README.md` - User-facing documentation
- `DEPLOYMENT.md` - Deployment instructions
- `QUICK_START.md` - Quick start guide

---

## 🐛 Known Issues & Solutions

### **Issue 1: Quote tokens not indexed**
- **Problem**: Small tokens not in API databases
- **Solution**: Use Zapper pool stats to calculate prices from reserves

### **Issue 2: LP pool addresses**
- **Problem**: 64-char addresses (pool contracts, not tokens)
- **Solution**: Query pool contracts directly via Zapper

### **Issue 3: Rate limiting**
- **Problem**: GeckoTerminal has 30 req/min limit
- **Solution**: Implement caching and batch requests

---

## 🔄 Data Flow Example

```
User → Dashboard UI
         ↓
    GET /v2/portfolio/summary
         ↓
    PortfolioService
         ↓
    ┌────┴─────┐
    ▼          ▼
UnifiedPrice  AlchemyService
   Service      (metadata)
    ↓
Try GeckoTerminal → Success! → Return data
    ↓ Failed
Try DeFiLlama → Failed
    ↓
Try Alchemy → Return metadata only
```

---

## 💡 Tips for Development

1. **Start backend first**: Get data flowing before building UI
2. **Test with real data**: Use DDD token for testing
3. **Handle errors gracefully**: APIs can fail, always have fallbacks
4. **Cache aggressively**: Reduce API calls, respect rate limits
5. **Log everything**: Makes debugging much easier
6. **Use TypeScript**: Catch errors early in frontend
7. **Component-driven**: Build UI in small, reusable pieces
8. **Mobile-first**: Design for mobile, scale up to desktop

---

## 🆘 Getting Help

- **API Issues**: Check `PRICE_API_IMPLEMENTATION.md`
- **Token Config**: See `token_config.py`
- **Strategy**: Read `DASHBOARD_STRATEGY.md`
- **Testing**: Run `python test_tokens.py`
- **Deployment**: Follow `DEPLOYMENT.md`

---

## 📞 Next Actions

**Immediate:**
1. Implement Zapper service
2. Add portfolio endpoints
3. Test LP pool data

**Short-term:**
4. Create frontend project
5. Build basic UI
6. Connect to API

**Long-term:**
7. Add advanced features
8. Optimize performance
9. Production deployment

---

## 🎉 Project Vision

Create a **professional-grade cryptocurrency analysis dashboard** that:
- Tracks DDD token and all its trading pairs
- Provides real-time price updates and historical charts
- Offers technical analysis and trading signals
- Handles obscure tokens that other platforms don't support
- Delivers a beautiful, intuitive user experience

**Let's build something amazing!** 🚀

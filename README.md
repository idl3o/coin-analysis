# Cryptocurrency Technical Analysis Dashboard

A full-stack web application for real-time cryptocurrency technical analysis with interactive charts and comprehensive indicators.

## Features

- **Real-time Price Tracking**: Monitor current prices for top cryptocurrencies
- **Technical Analysis Indicators**:
  - Moving Averages (SMA 20, 50, 200 & EMA 12, 26)
  - RSI (Relative Strength Index) with overbought/oversold signals
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands with bandwidth analysis
  - Volume trend analysis
- **Interactive Charts**: Historical price charts with customizable timeframes (7D, 30D, 90D, 180D)
- **Overall Trading Signal**: AI-calculated signal based on multiple indicators
- **Top Cryptocurrencies**: View and analyze top coins by market cap
- **Responsive Design**: Beautiful gradient UI that works on all devices

## 🚀 Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/coin-analysis)

This project is configured for one-click deployment to Vercel. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Quick Deploy Steps:**
1. Push your code to GitHub
2. Import to Vercel (vercel.com/new)
3. Deploy automatically - it just works! 🎉

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **pandas**: Data manipulation and analysis
- **pandas-ta**: Technical analysis indicators
- **CoinGecko API**: Free cryptocurrency data source
- **WebSockets**: Real-time price updates

### Frontend
- **React**: UI library
- **Vite**: Fast build tool
- **Recharts**: Beautiful responsive charts
- **Axios**: HTTP client
- **Lucide React**: Modern icon library

## Project Structure

```
coin-analysis/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── models/
│   │   └── schemas.py         # Pydantic data models
│   └── services/
│       ├── crypto_service.py  # CoinGecko API integration
│       ├── technical_analysis.py  # TA calculations
│       └── websocket_manager.py   # WebSocket handler
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── services/
        │   └── api.js         # API client
        └── components/
            ├── Header.jsx
            ├── Dashboard.jsx
            ├── CryptoSelector.jsx
            ├── CryptoCard.jsx
            ├── ChartView.jsx
            └── TechnicalIndicators.jsx
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

## Usage

1. **Start both servers** (backend and frontend)
2. **Open your browser** to `http://localhost:3000`
3. **Select a cryptocurrency** from the top selector
4. **Choose a timeframe** (7D, 30D, 90D, 180D)
5. **Analyze the data**:
   - View price chart with moving averages
   - Check technical indicators (RSI, MACD, Bollinger Bands)
   - Review overall trading signal
   - Monitor real-time price updates

## API Endpoints

### GET /api/crypto/price/{symbol}
Get current price for a cryptocurrency

### GET /api/crypto/prices?symbols=BTC,ETH,SOL
Get prices for multiple cryptocurrencies

### GET /api/crypto/historical/{symbol}?days=30&interval=daily
Get historical OHLCV data

### GET /api/crypto/indicators/{symbol}?days=30&interval=daily
Get technical analysis indicators

### GET /api/crypto/top?limit=20
Get top cryptocurrencies by market cap

### WebSocket /ws/{client_id}
Real-time price updates

## Supported Cryptocurrencies

Pre-configured symbols include:
- BTC (Bitcoin)
- ETH (Ethereum)
- BNB (Binance Coin)
- XRP (Ripple)
- ADA (Cardano)
- DOGE (Dogecoin)
- SOL (Solana)
- DOT (Polkadot)
- MATIC (Polygon)
- LTC (Litecoin)
- AVAX (Avalanche)
- LINK (Chainlink)
- UNI (Uniswap)
- ATOM (Cosmos)
- XLM (Stellar)

And many more available through the top cryptocurrencies list!

## Technical Indicators Explained

### RSI (Relative Strength Index)
- **Overbought**: RSI > 70 (potential sell signal)
- **Oversold**: RSI < 30 (potential buy signal)
- **Neutral**: RSI between 30-70

### MACD
- **Bullish**: MACD line crosses above signal line
- **Bearish**: MACD line crosses below signal line

### Moving Averages
- **SMA**: Simple Moving Average (20, 50, 200 periods)
- **EMA**: Exponential Moving Average (12, 26 periods)
- Used to identify trends and support/resistance levels

### Bollinger Bands
- Shows volatility and potential price breakouts
- Price touching upper band: potentially overbought
- Price touching lower band: potentially oversold

## Development

### Adding New Indicators

1. Add calculation method in `backend/services/technical_analysis.py`
2. Update the schema in `backend/models/schemas.py`
3. Add UI component in `frontend/src/components/TechnicalIndicators.jsx`

### Adding New Cryptocurrencies

Update the `symbol_map` in `backend/services/crypto_service.py:19`

## Building for Production

### Backend
```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
npm run build
```

The production files will be in the `dist` directory.

## Troubleshooting

### API Rate Limiting
CoinGecko free API has rate limits. If you encounter 429 errors, wait a few minutes before retrying.

### CORS Issues
Make sure the backend CORS middleware includes your frontend URL.

### Missing Dependencies
Ensure all dependencies are installed:
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## License

MIT License - feel free to use this project for learning and development!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational and informational purposes only. It does not provide financial advice. Always do your own research before making investment decisions.

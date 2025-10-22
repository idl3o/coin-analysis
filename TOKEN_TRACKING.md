# Custom Token Tracking Guide

## Overview

The Crypto Analysis Dashboard now supports tracking custom ERC-20 tokens by their contract address!

## Your Token

**Contract Address:** `0x4bf82cf0d6b2afc87367052b793097153c859d38`
**Platform:** Ethereum

## API Endpoints

### 1. Get Token Information by Contract Address

Fetch basic token information, price, and market data:

```bash
GET /api/crypto/token/contract/{contract_address}?platform=ethereum
```

**Example:**
```bash
curl "https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/contract/0x4bf82cf0d6b2afc87367052b793097153c859d38"
```

**Response includes:**
- Token symbol and name
- Current price (USD)
- Market cap
- 24h volume
- 24h price change
- Token image/logo
- CoinGecko coin_id (needed for other endpoints)

### 2. Get Historical Price Data

Once you have the `coin_id` from the first endpoint, get historical price data:

```bash
GET /api/crypto/token/{coin_id}/historical?days=30
```

**Example:**
```bash
curl "https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/YOUR_COIN_ID/historical?days=30"
```

**Parameters:**
- `days`: Number of days of historical data (1-365)

### 3. Get Technical Indicators

Get full technical analysis for the token:

```bash
GET /api/crypto/token/{coin_id}/indicators?days=30
```

**Example:**
```bash
curl "https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/YOUR_COIN_ID/indicators?days=30"
```

**Returns:**
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Moving Averages (SMA 20, 50, 200 & EMA 12, 26)
- Bollinger Bands
- Volume Trend
- Overall trading signal (bullish/bearish/neutral)

## Supported Platforms

- `ethereum` (default)
- `binance-smart-chain`
- `polygon-pos`
- `avalanche`
- `arbitrum-one`
- `optimistic-ethereum`
- And more blockchain platforms supported by CoinGecko

## Usage Workflow

### Step 1: Get Token Data
```bash
curl "https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/contract/0x4bf82cf0d6b2afc87367052b793097153c859d38"
```

Response will include the `coin_id` field.

### Step 2: Get Historical Data (using coin_id from Step 1)
```bash
curl "https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/{coin_id}/historical?days=30"
```

### Step 3: Get Technical Analysis (using coin_id from Step 1)
```bash
curl "https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/{coin_id}/indicators?days=90"
```

## JavaScript/Frontend Example

```javascript
// 1. Get token info by contract address
const contractAddress = '0x4bf82cf0d6b2afc87367052b793097153c859d38';

const response = await fetch(
  `https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/contract/${contractAddress}`
);

const tokenData = await response.json();
console.log('Token:', tokenData.name, tokenData.symbol);
console.log('Price:', tokenData.current_price);
console.log('Coin ID:', tokenData.coin_id);

// 2. Get technical indicators
const indicators = await fetch(
  `https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/${tokenData.coin_id}/indicators?days=30`
);

const analysis = await indicators.json();
console.log('RSI:', analysis.indicators.rsi);
console.log('Overall Signal:', analysis.indicators.overall_signal);
```

## Python Example

```python
import requests

# 1. Get token by contract address
contract = '0x4bf82cf0d6b2afc87367052b793097153c859d38'
url = f'https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/contract/{contract}'

response = requests.get(url)
token_data = response.json()

print(f"Token: {token_data['name']} ({token_data['symbol']})")
print(f"Price: ${token_data['current_price']}")
print(f"24h Change: {token_data['price_change_percentage_24h']}%")

# 2. Get technical analysis
coin_id = token_data['coin_id']
indicators_url = f'https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/{coin_id}/indicators?days=30'

indicators = requests.get(indicators_url).json()
print(f"\nRSI: {indicators['indicators']['rsi']['value']}")
print(f"Signal: {indicators['indicators']['rsi']['signal']}")
print(f"Overall: {indicators['indicators']['overall_signal']}")
```

## Error Handling

**Token not found (404):**
- Token contract address doesn't exist on CoinGecko
- Contract address is invalid
- Wrong platform specified

**Rate limiting (429):**
- CoinGecko free tier rate limits apply
- Wait a few minutes before retrying

**Server error (500):**
- Check the contract address format
- Ensure platform is spelled correctly

## Notes

- Token data is fetched from CoinGecko API
- Historical data availability depends on the token's listing on CoinGecko
- Some newer or smaller tokens may have limited historical data
- Technical indicators require at least 26 days of data for accurate calculations

## Live Deployment

**Base URL:** https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app

**Your Token Endpoint:**
```
https://coin-analysis-howjpsi5c-sam-ls-projects-54526df6.vercel.app/api/crypto/token/contract/0x4bf82cf0d6b2afc87367052b793097153c859d38
```

Try it in your browser or with curl to see live data!

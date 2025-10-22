import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd

class CryptoService:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    def _normalize_symbol(self, symbol: str) -> str:
        """Normalize cryptocurrency symbol to CoinGecko ID"""
        symbol_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "BNB": "binancecoin",
            "XRP": "ripple",
            "ADA": "cardano",
            "DOGE": "dogecoin",
            "SOL": "solana",
            "DOT": "polkadot",
            "MATIC": "matic-network",
            "LTC": "litecoin",
            "AVAX": "avalanche-2",
            "LINK": "chainlink",
            "UNI": "uniswap",
            "ATOM": "cosmos",
            "XLM": "stellar",
        }
        return symbol_map.get(symbol.upper(), symbol.lower())

    async def get_current_price(self, symbol: str) -> Dict:
        """Get current price for a single cryptocurrency"""
        session = await self._get_session()
        coin_id = self._normalize_symbol(symbol)

        url = f"{self.base_url}/coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false"
        }

        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                market_data = data.get("market_data", {})

                return {
                    "symbol": symbol.upper(),
                    "name": data.get("name", ""),
                    "current_price": market_data.get("current_price", {}).get("usd", 0),
                    "market_cap": market_data.get("market_cap", {}).get("usd"),
                    "volume_24h": market_data.get("total_volume", {}).get("usd"),
                    "price_change_24h": market_data.get("price_change_24h"),
                    "price_change_percentage_24h": market_data.get("price_change_percentage_24h"),
                    "last_updated": datetime.now().isoformat()
                }
            else:
                raise Exception(f"Failed to fetch price for {symbol}: {response.status}")

    async def get_multiple_prices(self, symbols: List[str]) -> List[Dict]:
        """Get current prices for multiple cryptocurrencies"""
        tasks = [self.get_current_price(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return successful results
        return [r for r in results if not isinstance(r, Exception)]

    async def get_historical_data(self, symbol: str, days: int = 30, interval: str = "daily") -> Dict:
        """Get historical OHLCV data for a cryptocurrency"""
        session = await self._get_session()
        coin_id = self._normalize_symbol(symbol)

        url = f"{self.base_url}/coins/{coin_id}/ohlc"
        params = {
            "vs_currency": "usd",
            "days": days
        }

        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()

                # Format data
                formatted_data = []
                for candle in data:
                    formatted_data.append({
                        "timestamp": candle[0],
                        "open": candle[1],
                        "high": candle[2],
                        "low": candle[3],
                        "close": candle[4],
                        "volume": 0  # CoinGecko OHLC doesn't include volume in this endpoint
                    })

                return {
                    "symbol": symbol.upper(),
                    "data": formatted_data
                }
            else:
                raise Exception(f"Failed to fetch historical data for {symbol}: {response.status}")

    async def get_token_by_contract(self, contract_address: str, platform: str = "ethereum") -> Dict:
        """Get token data by contract address"""
        session = await self._get_session()

        url = f"{self.base_url}/coins/{platform}/contract/{contract_address.lower()}"

        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                market_data = data.get("market_data", {})

                return {
                    "symbol": data.get("symbol", "").upper(),
                    "name": data.get("name", ""),
                    "contract_address": contract_address,
                    "platform": platform,
                    "current_price": market_data.get("current_price", {}).get("usd", 0),
                    "market_cap": market_data.get("market_cap", {}).get("usd"),
                    "volume_24h": market_data.get("total_volume", {}).get("usd"),
                    "price_change_24h": market_data.get("price_change_24h"),
                    "price_change_percentage_24h": market_data.get("price_change_percentage_24h"),
                    "image": data.get("image", {}).get("small"),
                    "coin_id": data.get("id"),
                    "last_updated": datetime.now().isoformat()
                }
            else:
                raise Exception(f"Failed to fetch token {contract_address}: {response.status}")

    async def get_token_historical_data(self, coin_id: str, days: int = 30) -> Dict:
        """Get historical OHLCV data for a token by coin_id"""
        session = await self._get_session()

        url = f"{self.base_url}/coins/{coin_id}/ohlc"
        params = {
            "vs_currency": "usd",
            "days": days
        }

        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()

                # Format data
                formatted_data = []
                for candle in data:
                    formatted_data.append({
                        "timestamp": candle[0],
                        "open": candle[1],
                        "high": candle[2],
                        "low": candle[3],
                        "close": candle[4],
                        "volume": 0
                    })

                return {
                    "symbol": coin_id.upper(),
                    "data": formatted_data
                }
            else:
                raise Exception(f"Failed to fetch historical data for {coin_id}: {response.status}")

    async def get_top_cryptocurrencies(self, limit: int = 20) -> List[Dict]:
        """Get top cryptocurrencies by market cap"""
        session = await self._get_session()

        url = f"{self.base_url}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": "false"
        }

        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()

                return [{
                    "symbol": coin.get("symbol", "").upper(),
                    "name": coin.get("name", ""),
                    "current_price": coin.get("current_price", 0),
                    "market_cap": coin.get("market_cap"),
                    "volume_24h": coin.get("total_volume"),
                    "price_change_24h": coin.get("price_change_24h"),
                    "price_change_percentage_24h": coin.get("price_change_percentage_24h"),
                    "market_cap_rank": coin.get("market_cap_rank"),
                    "image": coin.get("image"),
                    "last_updated": coin.get("last_updated")
                } for coin in data]
            else:
                raise Exception(f"Failed to fetch top cryptocurrencies: {response.status}")

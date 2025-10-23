import aiohttp
import asyncio
from typing import Dict, Optional, List
from datetime import datetime

class GeckoTerminalService:
    """
    GeckoTerminal API service for getting custom token prices from DEXs.
    Free tier: 30 calls/minute
    Supports 1,700+ DEXs across 250+ networks
    """

    def __init__(self):
        self.base_url = "https://api.geckoterminal.com/api/v2"
        self.session: Optional[aiohttp.ClientSession] = None

        # Network mapping
        self.network_map = {
            "ethereum": "eth",
            "polygon": "polygon_pos",
            "base": "base",
            "arbitrum": "arbitrum",
            "optimism": "optimism",
            "bsc": "bsc",
            "avalanche": "avax"
        }

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    def _get_network_id(self, network: str) -> str:
        """Convert network name to GeckoTerminal network ID"""
        return self.network_map.get(network.lower(), network.lower())

    async def get_token_price(self, contract_address: str, network: str = "polygon") -> Dict:
        """
        Get current price and market data for a token by contract address.

        Args:
            contract_address: Token contract address
            network: Network name (ethereum, polygon, base, arbitrum, etc.)

        Returns:
            Dict with price, volume, liquidity, and metadata
        """
        session = await self._get_session()
        network_id = self._get_network_id(network)

        url = f"{self.base_url}/networks/{network_id}/tokens/{contract_address.lower()}"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    token_data = data.get('data', {})
                    attributes = token_data.get('attributes', {})

                    # Get the most liquid pool for this token
                    pools = await self._get_token_pools(contract_address, network)
                    top_pool = pools[0] if pools else {}

                    return {
                        "contract_address": contract_address,
                        "network": network,
                        "name": attributes.get('name', ''),
                        "symbol": attributes.get('symbol', ''),
                        "current_price": float(attributes.get('price_usd', 0)) if attributes.get('price_usd') else 0,
                        "price_change_24h": float(attributes.get('price_change_percentage', {}).get('h24', 0)),
                        "volume_24h": float(top_pool.get('volume_24h', 0)) if top_pool else 0,
                        "liquidity_usd": float(top_pool.get('reserve_in_usd', 0)) if top_pool else 0,
                        "market_cap": None,  # GeckoTerminal doesn't provide market cap
                        "fdv_usd": float(attributes.get('fdv_usd', 0)) if attributes.get('fdv_usd') else None,
                        "image_url": attributes.get('image_url'),
                        "coingecko_coin_id": attributes.get('coingecko_coin_id'),
                        "top_pool_address": top_pool.get('address') if top_pool else None,
                        "last_updated": datetime.now().isoformat(),
                        "source": "geckoterminal"
                    }
                elif response.status == 404:
                    raise Exception(f"Token not found on {network}")
                else:
                    error_text = await response.text()
                    raise Exception(f"GeckoTerminal API error: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to fetch token from GeckoTerminal: {str(e)}")

    async def _get_token_pools(self, contract_address: str, network: str = "polygon") -> List[Dict]:
        """Get all pools for a token, sorted by liquidity"""
        session = await self._get_session()
        network_id = self._get_network_id(network)

        url = f"{self.base_url}/networks/{network_id}/tokens/{contract_address.lower()}/pools"
        params = {
            "page": 1
        }

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    pools_data = data.get('data', [])

                    pools = []
                    for pool in pools_data:
                        attrs = pool.get('attributes', {})
                        pools.append({
                            "address": pool.get('id', '').split('_')[-1] if pool.get('id') else '',
                            "name": attrs.get('name', ''),
                            "dex": attrs.get('dex_id', ''),
                            "reserve_in_usd": attrs.get('reserve_in_usd', '0'),
                            "volume_24h": attrs.get('volume_usd', {}).get('h24', '0'),
                            "price_usd": attrs.get('base_token_price_usd', '0')
                        })

                    return pools
                else:
                    return []
        except Exception:
            return []

    async def get_historical_ohlcv(
        self,
        pool_address: str,
        network: str = "polygon",
        timeframe: str = "day",
        aggregate: int = 1,
        limit: int = 30
    ) -> Dict:
        """
        Get historical OHLCV data for a token pool.

        Args:
            pool_address: Pool contract address
            network: Network name
            timeframe: minute, hour, day (default: day)
            aggregate: Aggregation (1, 5, 15 for minutes; 1, 4, 12 for hours; 1 for day)
            limit: Number of candles (max 1000)

        Returns:
            Dict with OHLCV data
        """
        session = await self._get_session()
        network_id = self._get_network_id(network)

        url = f"{self.base_url}/networks/{network_id}/pools/{pool_address.lower()}/ohlcv/{timeframe}"
        params = {
            "aggregate": aggregate,
            "limit": limit,
            "currency": "usd"
        }

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    ohlcv_data = data.get('data', {}).get('attributes', {}).get('ohlcv_list', [])

                    formatted_data = []
                    for candle in ohlcv_data:
                        formatted_data.append({
                            "timestamp": candle[0] * 1000,  # Convert to milliseconds
                            "open": float(candle[1]),
                            "high": float(candle[2]),
                            "low": float(candle[3]),
                            "close": float(candle[4]),
                            "volume": float(candle[5])
                        })

                    return {
                        "pool_address": pool_address,
                        "network": network,
                        "timeframe": timeframe,
                        "data": formatted_data
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to fetch OHLCV: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to fetch historical data from GeckoTerminal: {str(e)}")

    async def get_token_with_ohlcv(self, contract_address: str, network: str = "polygon", days: int = 30) -> Dict:
        """
        Get token price info along with historical OHLCV data.

        Args:
            contract_address: Token contract address
            network: Network name
            days: Number of days of historical data

        Returns:
            Combined dict with current price and historical data
        """
        # Get current price and find top pool
        price_data = await self.get_token_price(contract_address, network)

        # If we have a top pool, get its OHLCV data
        if price_data.get('top_pool_address'):
            try:
                ohlcv_data = await self.get_historical_ohlcv(
                    pool_address=price_data['top_pool_address'],
                    network=network,
                    timeframe="day",
                    limit=days
                )
                price_data['historical_data'] = ohlcv_data.get('data', [])
            except Exception as e:
                price_data['historical_data'] = []
                price_data['historical_error'] = str(e)
        else:
            price_data['historical_data'] = []

        return price_data

    async def search_pools(self, query: str, network: Optional[str] = None) -> List[Dict]:
        """
        Search for pools by token name or symbol.

        Args:
            query: Search query (token name or symbol)
            network: Optional network filter

        Returns:
            List of matching pools
        """
        session = await self._get_session()

        url = f"{self.base_url}/search/pools"
        params = {
            "query": query,
            "network": self._get_network_id(network) if network else None,
            "page": 1
        }

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    pools_data = data.get('data', [])

                    results = []
                    for pool in pools_data:
                        attrs = pool.get('attributes', {})
                        results.append({
                            "address": pool.get('id', '').split('_')[-1] if pool.get('id') else '',
                            "name": attrs.get('name', ''),
                            "network": pool.get('id', '').split('_')[0] if pool.get('id') else '',
                            "dex": attrs.get('dex_id', ''),
                            "base_token_symbol": attrs.get('base_token_price_quote_token', ''),
                            "quote_token_symbol": attrs.get('quote_token_price_quote_token', ''),
                            "price_usd": attrs.get('base_token_price_usd', '0'),
                            "reserve_in_usd": attrs.get('reserve_in_usd', '0')
                        })

                    return results
                else:
                    return []
        except Exception:
            return []

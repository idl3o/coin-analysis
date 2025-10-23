import aiohttp
import asyncio
from typing import Dict, Optional, List
from datetime import datetime, timedelta

class DeFiLlamaService:
    """
    DeFiLlama API service for pricing exotic and hard-to-price tokens.
    Free tier available.
    Specializes in LP tokens, exotic tokens, and on-chain price calculations.
    """

    def __init__(self):
        self.base_url = "https://coins.llama.fi"
        self.session: Optional[aiohttp.ClientSession] = None

        # Platform/chain mapping
        self.chain_map = {
            "ethereum": "ethereum",
            "polygon": "polygon",
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

    def _get_chain_id(self, network: str) -> str:
        """Convert network name to DeFiLlama chain ID"""
        return self.chain_map.get(network.lower(), network.lower())

    def _format_coin_id(self, contract_address: str, network: str) -> str:
        """Format coin ID for DeFiLlama API (chain:address)"""
        chain_id = self._get_chain_id(network)
        return f"{chain_id}:{contract_address.lower()}"

    async def get_token_price(self, contract_address: str, network: str = "polygon") -> Dict:
        """
        Get current price for a token using DeFiLlama.

        Args:
            contract_address: Token contract address
            network: Network name

        Returns:
            Dict with price and metadata
        """
        session = await self._get_session()
        coin_id = self._format_coin_id(contract_address, network)

        url = f"{self.base_url}/prices/current/{coin_id}"
        params = {
            "searchWidth": "4h"  # Search within 4 hours for price data
        }

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    coin_data = data.get('coins', {}).get(coin_id, {})

                    if not coin_data:
                        raise Exception(f"No price data found for {coin_id}")

                    return {
                        "contract_address": contract_address,
                        "network": network,
                        "symbol": coin_data.get('symbol', ''),
                        "current_price": float(coin_data.get('price', 0)),
                        "decimals": coin_data.get('decimals'),
                        "timestamp": coin_data.get('timestamp'),
                        "confidence": coin_data.get('confidence', 0),
                        "last_updated": datetime.now().isoformat(),
                        "source": "defillama"
                    }
                elif response.status == 404:
                    raise Exception(f"Token not found on DeFiLlama")
                else:
                    error_text = await response.text()
                    raise Exception(f"DeFiLlama API error: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to fetch token from DeFiLlama: {str(e)}")

    async def get_multiple_token_prices(self, tokens: List[tuple]) -> Dict[str, Dict]:
        """
        Get prices for multiple tokens at once.

        Args:
            tokens: List of (contract_address, network) tuples

        Returns:
            Dict mapping coin_id to price data
        """
        session = await self._get_session()

        # Format coin IDs
        coin_ids = [self._format_coin_id(addr, net) for addr, net in tokens]
        coins_param = ",".join(coin_ids)

        url = f"{self.base_url}/prices/current/{coins_param}"
        params = {
            "searchWidth": "4h"
        }

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    coins_data = data.get('coins', {})

                    results = {}
                    for coin_id, coin_data in coins_data.items():
                        # Extract address and network from coin_id
                        chain, address = coin_id.split(':')

                        results[coin_id] = {
                            "contract_address": address,
                            "network": chain,
                            "symbol": coin_data.get('symbol', ''),
                            "current_price": float(coin_data.get('price', 0)),
                            "decimals": coin_data.get('decimals'),
                            "timestamp": coin_data.get('timestamp'),
                            "confidence": coin_data.get('confidence', 0),
                            "last_updated": datetime.now().isoformat(),
                            "source": "defillama"
                        }

                    return results
                else:
                    return {}
        except Exception:
            return {}

    async def get_historical_prices(
        self,
        contract_address: str,
        network: str = "polygon",
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
        span: Optional[int] = None,
        period: str = "1d"
    ) -> Dict:
        """
        Get historical price data for a token.

        Args:
            contract_address: Token contract address
            network: Network name
            start_timestamp: Start timestamp (unix)
            end_timestamp: End timestamp (unix)
            span: Number of data points to return
            period: Time period between data points (e.g., '1d', '1h')

        Returns:
            Dict with historical price data
        """
        session = await self._get_session()
        coin_id = self._format_coin_id(contract_address, network)

        url = f"{self.base_url}/chart/{coin_id}"
        params = {}

        if start_timestamp:
            params['start'] = start_timestamp
        if end_timestamp:
            params['end'] = end_timestamp
        if span:
            params['span'] = span
        if period:
            params['period'] = period

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    coins_data = data.get('coins', {}).get(coin_id, {})

                    if not coins_data:
                        raise Exception(f"No historical data found for {coin_id}")

                    prices = coins_data.get('prices', [])
                    symbol = coins_data.get('symbol', '')
                    decimals = coins_data.get('decimals')

                    formatted_data = []
                    for price_point in prices:
                        formatted_data.append({
                            "timestamp": price_point.get('timestamp', 0) * 1000,  # Convert to ms
                            "price": float(price_point.get('price', 0)),
                            "confidence": price_point.get('confidence', 0)
                        })

                    return {
                        "contract_address": contract_address,
                        "network": network,
                        "symbol": symbol,
                        "decimals": decimals,
                        "data": formatted_data,
                        "source": "defillama"
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to fetch historical data: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to fetch historical data from DeFiLlama: {str(e)}")

    async def get_token_price_at_timestamp(
        self,
        contract_address: str,
        network: str,
        timestamp: int
    ) -> Dict:
        """
        Get token price at a specific timestamp.

        Args:
            contract_address: Token contract address
            network: Network name
            timestamp: Unix timestamp

        Returns:
            Dict with price at that timestamp
        """
        session = await self._get_session()
        coin_id = self._format_coin_id(contract_address, network)

        url = f"{self.base_url}/prices/historical/{timestamp}/{coin_id}"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    coin_data = data.get('coins', {}).get(coin_id, {})

                    if not coin_data:
                        raise Exception(f"No price data found for {coin_id} at timestamp {timestamp}")

                    return {
                        "contract_address": contract_address,
                        "network": network,
                        "symbol": coin_data.get('symbol', ''),
                        "price": float(coin_data.get('price', 0)),
                        "timestamp": timestamp,
                        "confidence": coin_data.get('confidence', 0),
                        "source": "defillama"
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to fetch historical price: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to fetch price at timestamp from DeFiLlama: {str(e)}")

    async def get_percentage_change(
        self,
        contract_address: str,
        network: str,
        lookback_hours: int = 24
    ) -> Dict:
        """
        Get price percentage change over a time period.

        Args:
            contract_address: Token contract address
            network: Network name
            lookback_hours: Hours to look back (default: 24)

        Returns:
            Dict with current price and percentage change
        """
        session = await self._get_session()
        coin_id = self._format_coin_id(contract_address, network)

        url = f"{self.base_url}/percentage/{coin_id}"
        params = {
            "lookForward": "false",
            "timestamp": int(datetime.now().timestamp())
        }

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    return {
                        "contract_address": contract_address,
                        "network": network,
                        "percentage_change": data,
                        "lookback_hours": lookback_hours,
                        "source": "defillama"
                    }
                else:
                    return {
                        "contract_address": contract_address,
                        "network": network,
                        "percentage_change": None,
                        "error": "Failed to fetch percentage change"
                    }
        except Exception as e:
            return {
                "contract_address": contract_address,
                "network": network,
                "percentage_change": None,
                "error": str(e)
            }

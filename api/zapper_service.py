import aiohttp
import asyncio
from typing import Dict, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ZapperService:
    """
    Zapper API service for DeFi portfolio tracking and LP pool data.

    Zapper provides:
    - Token balances across DeFi protocols
    - LP pool statistics and positions
    - NFT holdings
    - Transaction history
    - Real-time portfolio valuation

    API Docs: https://studio.zapper.xyz/docs/apis/api-syntax
    """

    def __init__(self, api_key: Optional[str] = None):
        # Zapper API endpoints
        self.base_url = "https://api.zapper.xyz"
        self.api_key = api_key  # Optional - some endpoints work without key
        self.session: Optional[aiohttp.ClientSession] = None

        # Network mapping to Zapper network IDs
        self.network_map = {
            "ethereum": "ethereum",
            "polygon": "polygon",
            "optimism": "optimism",
            "arbitrum": "arbitrum",
            "base": "base",
            "bsc": "binance-smart-chain",
            "avalanche": "avalanche"
        }

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Basic {self.api_key}"
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    def _get_network_id(self, network: str) -> str:
        """Convert network name to Zapper network ID"""
        return self.network_map.get(network.lower(), network.lower())

    async def get_token_balances(
        self,
        wallet_address: str,
        network: str = "polygon"
    ) -> Dict:
        """
        Get token balances for a wallet address.

        Args:
            wallet_address: Wallet address to query
            network: Network name

        Returns:
            Dict with token balances and values
        """
        session = await self._get_session()
        network_id = self._get_network_id(network)

        # Zapper v2 balance endpoint
        url = f"{self.base_url}/v2/balances"
        params = {
            "addresses[]": wallet_address,
            "networks[]": network_id
        }

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "wallet": wallet_address,
                        "network": network,
                        "balances": data,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Zapper API error: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to fetch balances from Zapper: {str(e)}")

    async def get_token_price(
        self,
        token_address: str,
        network: str = "polygon"
    ) -> Dict:
        """
        Get token price from Zapper.

        Args:
            token_address: Token contract address
            network: Network name

        Returns:
            Dict with token price data
        """
        session = await self._get_session()
        network_id = self._get_network_id(network)

        # Zapper token price endpoint
        url = f"{self.base_url}/v2/prices"
        params = {
            "network": network_id,
            "tokenAddress": token_address.lower()
        }

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    # Zapper returns price data in various formats
                    price = data.get("price", 0)

                    return {
                        "token_address": token_address,
                        "network": network,
                        "price_usd": float(price) if price else 0,
                        "timestamp": datetime.now().isoformat(),
                        "source": "zapper",
                        "raw_data": data
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Zapper API error: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to fetch price from Zapper: {str(e)}")

    async def get_pool_stats(
        self,
        pool_address: str,
        network: str = "polygon",
        dex: str = "uniswap-v2"
    ) -> Dict:
        """
        Get liquidity pool statistics.

        Args:
            pool_address: LP pool contract address
            network: Network name
            dex: DEX name (uniswap-v2, sushiswap, quickswap, etc.)

        Returns:
            Dict with pool statistics (reserves, liquidity, volume, etc.)
        """
        session = await self._get_session()
        network_id = self._get_network_id(network)

        # For pool stats, we might need to query app positions
        # Zapper treats LP positions as "app" positions
        url = f"{self.base_url}/v2/apps/{dex}/positions"
        params = {
            "addresses[]": pool_address,
            "network": network_id
        }

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    return {
                        "pool_address": pool_address,
                        "network": network,
                        "dex": dex,
                        "stats": data,
                        "timestamp": datetime.now().isoformat(),
                        "source": "zapper"
                    }
                else:
                    error_text = await response.text()
                    logger.warning(f"Failed to get pool stats: {response.status} - {error_text}")
                    return {
                        "pool_address": pool_address,
                        "network": network,
                        "error": f"API returned {response.status}",
                        "note": "Pool might not be tracked by Zapper or DEX name incorrect"
                    }
        except Exception as e:
            logger.error(f"Pool stats error: {str(e)}")
            return {
                "pool_address": pool_address,
                "network": network,
                "error": str(e)
            }

    async def calculate_token_price_from_pool(
        self,
        pool_address: str,
        token0_address: str,
        token1_address: str,
        token0_known_price: float,
        network: str = "polygon"
    ) -> Dict:
        """
        Calculate token1 price based on pool reserves and token0 known price.

        Formula: token1_price = (reserve0 * token0_price) / reserve1

        Args:
            pool_address: LP pool contract address
            token0_address: First token in pair (with known price)
            token1_address: Second token in pair (price to calculate)
            token0_known_price: Known price of token0
            network: Network name

        Returns:
            Dict with calculated price and pool data
        """
        # This would require getting pool reserves
        # For now, returning a placeholder structure
        return {
            "pool_address": pool_address,
            "token0": token0_address,
            "token1": token1_address,
            "token1_calculated_price": None,
            "calculation_method": "pool_reserves",
            "note": "Requires pool reserve data - to be implemented with contract calls"
        }

    async def search_apps(self, query: str, network: Optional[str] = None) -> List[Dict]:
        """
        Search for DeFi apps/protocols on Zapper.

        Args:
            query: Search query (app name)
            network: Optional network filter

        Returns:
            List of matching apps
        """
        session = await self._get_session()

        url = f"{self.base_url}/v2/apps"
        params = {}
        if network:
            params["network"] = self._get_network_id(network)

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    # Filter by query
                    if query:
                        query_lower = query.lower()
                        filtered = [
                            app for app in data
                            if query_lower in app.get("id", "").lower() or
                               query_lower in app.get("name", "").lower()
                        ]
                        return filtered

                    return data
                else:
                    return []
        except Exception as e:
            logger.error(f"App search error: {str(e)}")
            return []

    async def get_supported_dexes(self, network: str = "polygon") -> List[str]:
        """
        Get list of supported DEXes on a network.

        Args:
            network: Network name

        Returns:
            List of DEX IDs that Zapper supports
        """
        # Common DEXes on Polygon
        polygon_dexes = [
            "uniswap-v2",
            "uniswap-v3",
            "sushiswap",
            "quickswap",
            "quickswap-v3",
            "balancer-v2",
            "curve",
            "dfyn",
            "polydex"
        ]

        # For now, return common DEXes
        # In production, this would query Zapper's apps API
        if network.lower() == "polygon":
            return polygon_dexes
        else:
            return ["uniswap-v2", "uniswap-v3", "sushiswap"]

    async def get_portfolio_value(
        self,
        wallet_address: str,
        networks: Optional[List[str]] = None
    ) -> Dict:
        """
        Get total portfolio value across all networks and protocols.

        Args:
            wallet_address: Wallet address
            networks: List of networks to check (default: all)

        Returns:
            Dict with total portfolio value and breakdown
        """
        if networks is None:
            networks = ["polygon", "ethereum"]

        session = await self._get_session()

        # Zapper v2 balance endpoint with network aggregation
        network_ids = [self._get_network_id(n) for n in networks]

        url = f"{self.base_url}/v2/balances"
        params = {
            "addresses[]": wallet_address
        }
        for net_id in network_ids:
            params[f"networks[]"] = net_id

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    # Calculate total value
                    total_value = 0
                    breakdown = []

                    # This would need proper parsing of Zapper's response
                    # Placeholder structure
                    return {
                        "wallet": wallet_address,
                        "total_value_usd": total_value,
                        "networks": networks,
                        "breakdown": breakdown,
                        "timestamp": datetime.now().isoformat(),
                        "raw_data": data
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Zapper API error: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Failed to fetch portfolio from Zapper: {str(e)}")

    async def health_check(self) -> Dict:
        """
        Check if Zapper API is accessible.

        Returns:
            Dict with health status
        """
        session = await self._get_session()

        try:
            # Try to access apps endpoint as health check
            async with session.get(f"{self.base_url}/v2/apps", timeout=5) as response:
                return {
                    "status": "healthy" if response.status == 200 else "degraded",
                    "status_code": response.status,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

import aiohttp
import asyncio
from typing import Dict, Optional
from datetime import datetime
import os

class AlchemyService:
    def __init__(self, api_key: Optional[str] = None, network: str = "polygon"):
        self.api_key = api_key or os.environ.get('ALCHEMY_API_KEY')

        # Network URL mapping
        network_urls = {
            "ethereum": f"https://eth-mainnet.g.alchemy.com/v2/{self.api_key}",
            "polygon": f"https://polygon-mainnet.g.alchemy.com/v2/{self.api_key}",
            "base": f"https://base-mainnet.g.alchemy.com/v2/{self.api_key}",
            "arbitrum": f"https://arb-mainnet.g.alchemy.com/v2/{self.api_key}",
        }

        self.base_url = network_urls.get(network, network_urls["polygon"])
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def get_token_metadata(self, contract_address: str) -> Dict:
        """Get token metadata using Alchemy API"""
        session = await self._get_session()

        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "alchemy_getTokenMetadata",
            "params": [contract_address]
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            async with session.post(self.base_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data.get('result', {})

                    return {
                        "symbol": result.get('symbol', ''),
                        "name": result.get('name', ''),
                        "decimals": result.get('decimals'),
                        "logo": result.get('logo'),
                        "contract_address": contract_address,
                        "last_updated": datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to fetch token metadata: {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Alchemy API error: {str(e)}")

    async def get_token_balances(self, address: str, contract_addresses: list) -> Dict:
        """Get token balances for specific contract addresses"""
        session = await self._get_session()

        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "alchemy_getTokenBalances",
            "params": [address, contract_addresses]
        }

        try:
            async with session.post(self.base_url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('result', {})
                else:
                    raise Exception(f"Failed to fetch token balances: {response.status}")
        except Exception as e:
            raise Exception(f"Alchemy API error: {str(e)}")

    async def get_token_price(self, contract_address: str) -> Dict:
        """Get token price data - Note: Alchemy doesn't provide price data directly.
        This would need to be supplemented with a DEX price oracle or another service."""

        # Get metadata first
        metadata = await self.get_token_metadata(contract_address)

        # For price data, you'd typically integrate with:
        # - Uniswap/DEX APIs for token prices
        # - CoinGecko as a fallback
        # - Or use a price oracle service

        return {
            **metadata,
            "current_price": None,  # Would need price oracle integration
            "price_change_24h": None,
            "volume_24h": None,
            "market_cap": None
        }

import asyncio
from typing import Dict, Optional, List
from datetime import datetime
import logging

from geckoterminal_service import GeckoTerminalService
from defillama_service import DeFiLlamaService
from alchemy_service import AlchemyService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedPriceService:
    """
    Unified service that orchestrates multiple price data sources with intelligent fallback.

    Priority order:
    1. GeckoTerminal (free, comprehensive DEX data)
    2. DeFiLlama (free, handles exotic tokens)
    3. Alchemy (metadata only, no price data)

    This service tries each source in order and returns the first successful result.
    """

    def __init__(self, alchemy_api_key: Optional[str] = None):
        self.geckoterminal = GeckoTerminalService()
        self.defillama = DeFiLlamaService()
        self.alchemy = AlchemyService(api_key=alchemy_api_key)

    async def close(self):
        """Close all service sessions"""
        await self.geckoterminal.close()
        await self.defillama.close()
        await self.alchemy.close()

    async def get_token_price(
        self,
        contract_address: str,
        network: str = "polygon",
        include_metadata: bool = True
    ) -> Dict:
        """
        Get token price with automatic fallback between sources.

        Args:
            contract_address: Token contract address
            network: Network name (ethereum, polygon, base, arbitrum, etc.)
            include_metadata: If True, fetches metadata from Alchemy if price sources fail

        Returns:
            Dict with price, volume, liquidity, and metadata from best available source
        """
        errors = []

        # Try 1: GeckoTerminal (best for DEX tokens)
        try:
            logger.info(f"Trying GeckoTerminal for {contract_address} on {network}")
            data = await self.geckoterminal.get_token_price(contract_address, network)
            logger.info(f"✓ GeckoTerminal succeeded for {contract_address}")
            return data
        except Exception as e:
            error_msg = f"GeckoTerminal failed: {str(e)}"
            logger.warning(error_msg)
            errors.append(error_msg)

        # Try 2: DeFiLlama (fallback for exotic tokens)
        try:
            logger.info(f"Trying DeFiLlama for {contract_address} on {network}")
            data = await self.defillama.get_token_price(contract_address, network)
            logger.info(f"✓ DeFiLlama succeeded for {contract_address}")

            # DeFiLlama has limited data, so we might want to enrich with Alchemy metadata
            if include_metadata:
                try:
                    alchemy_data = await self.alchemy.get_token_metadata(contract_address)
                    data['name'] = alchemy_data.get('name', data.get('symbol', ''))
                    data['logo'] = alchemy_data.get('logo')
                    data['decimals'] = alchemy_data.get('decimals', data.get('decimals'))
                except Exception:
                    pass  # Alchemy metadata is optional

            return data
        except Exception as e:
            error_msg = f"DeFiLlama failed: {str(e)}"
            logger.warning(error_msg)
            errors.append(error_msg)

        # Try 3: Alchemy (metadata only, no price)
        if include_metadata:
            try:
                logger.info(f"Trying Alchemy for metadata of {contract_address} on {network}")
                data = await self.alchemy.get_token_metadata(contract_address)
                logger.info(f"✓ Alchemy succeeded for {contract_address} (metadata only)")

                # Return metadata with no price data
                return {
                    "contract_address": contract_address,
                    "network": network,
                    "name": data.get('name', ''),
                    "symbol": data.get('symbol', ''),
                    "decimals": data.get('decimals'),
                    "logo": data.get('logo'),
                    "current_price": None,
                    "price_change_24h": None,
                    "volume_24h": None,
                    "liquidity_usd": None,
                    "market_cap": None,
                    "last_updated": data.get('last_updated'),
                    "source": "alchemy",
                    "note": "Price data unavailable - metadata only"
                }
            except Exception as e:
                error_msg = f"Alchemy failed: {str(e)}"
                logger.warning(error_msg)
                errors.append(error_msg)

        # All sources failed
        raise Exception(f"All price sources failed for {contract_address} on {network}. Errors: {'; '.join(errors)}")

    async def get_token_with_historical(
        self,
        contract_address: str,
        network: str = "polygon",
        days: int = 30
    ) -> Dict:
        """
        Get token price with historical OHLCV data.

        Args:
            contract_address: Token contract address
            network: Network name
            days: Number of days of historical data

        Returns:
            Dict with current price and historical data
        """
        errors = []

        # Try 1: GeckoTerminal (has OHLCV data)
        try:
            logger.info(f"Trying GeckoTerminal with OHLCV for {contract_address}")
            data = await self.geckoterminal.get_token_with_ohlcv(contract_address, network, days)
            logger.info(f"✓ GeckoTerminal with OHLCV succeeded")
            return data
        except Exception as e:
            error_msg = f"GeckoTerminal OHLCV failed: {str(e)}"
            logger.warning(error_msg)
            errors.append(error_msg)

        # Try 2: DeFiLlama (has historical prices)
        try:
            logger.info(f"Trying DeFiLlama with historical data for {contract_address}")

            # Get current price
            current = await self.defillama.get_token_price(contract_address, network)

            # Get historical data
            historical = await self.defillama.get_historical_prices(
                contract_address,
                network,
                span=days
            )

            # Combine
            current['historical_data'] = historical.get('data', [])
            logger.info(f"✓ DeFiLlama with historical succeeded")
            return current
        except Exception as e:
            error_msg = f"DeFiLlama historical failed: {str(e)}"
            logger.warning(error_msg)
            errors.append(error_msg)

        # Try 3: Just get current price without historical
        try:
            logger.info(f"Falling back to current price only for {contract_address}")
            data = await self.get_token_price(contract_address, network)
            data['historical_data'] = []
            data['note'] = "Historical data unavailable"
            return data
        except Exception as e:
            error_msg = f"Current price fallback failed: {str(e)}"
            logger.warning(error_msg)
            errors.append(error_msg)

        raise Exception(f"All sources failed for historical data. Errors: {'; '.join(errors)}")

    async def get_multiple_tokens(
        self,
        tokens: List[tuple],
        include_metadata: bool = True
    ) -> List[Dict]:
        """
        Get prices for multiple tokens concurrently.

        Args:
            tokens: List of (contract_address, network) tuples
            include_metadata: Include Alchemy metadata

        Returns:
            List of token price data dicts
        """
        tasks = [
            self.get_token_price(addr, net, include_metadata)
            for addr, net in tokens
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return successful results
        successful = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                addr, net = tokens[i]
                logger.error(f"Failed to get price for {addr} on {net}: {str(result)}")
            else:
                successful.append(result)

        return successful

    async def compare_sources(
        self,
        contract_address: str,
        network: str = "polygon"
    ) -> Dict:
        """
        Compare prices from all available sources (for debugging/validation).

        Args:
            contract_address: Token contract address
            network: Network name

        Returns:
            Dict with results from all sources
        """
        results = {
            "contract_address": contract_address,
            "network": network,
            "timestamp": datetime.now().isoformat(),
            "sources": {}
        }

        # Try GeckoTerminal
        try:
            gecko_data = await self.geckoterminal.get_token_price(contract_address, network)
            results['sources']['geckoterminal'] = {
                "success": True,
                "price": gecko_data.get('current_price'),
                "data": gecko_data
            }
        except Exception as e:
            results['sources']['geckoterminal'] = {
                "success": False,
                "error": str(e)
            }

        # Try DeFiLlama
        try:
            llama_data = await self.defillama.get_token_price(contract_address, network)
            results['sources']['defillama'] = {
                "success": True,
                "price": llama_data.get('current_price'),
                "data": llama_data
            }
        except Exception as e:
            results['sources']['defillama'] = {
                "success": False,
                "error": str(e)
            }

        # Try Alchemy (metadata only)
        try:
            alchemy_data = await self.alchemy.get_token_metadata(contract_address)
            results['sources']['alchemy'] = {
                "success": True,
                "price": None,
                "data": alchemy_data,
                "note": "Metadata only, no price"
            }
        except Exception as e:
            results['sources']['alchemy'] = {
                "success": False,
                "error": str(e)
            }

        # Calculate price discrepancy if multiple sources have prices
        prices = []
        for source, data in results['sources'].items():
            if data.get('success') and data.get('price') is not None:
                prices.append((source, data['price']))

        if len(prices) > 1:
            price_values = [p[1] for p in prices]
            avg_price = sum(price_values) / len(price_values)
            max_deviation = max(abs(p - avg_price) / avg_price * 100 for p in price_values)

            results['price_analysis'] = {
                "prices": prices,
                "average": avg_price,
                "max_deviation_percent": max_deviation,
                "consistent": max_deviation < 5  # Less than 5% deviation
            }

        return results

    async def health_check(self) -> Dict:
        """
        Check health of all price sources.

        Returns:
            Dict with status of each service
        """
        health = {
            "timestamp": datetime.now().isoformat(),
            "services": {}
        }

        # Test GeckoTerminal with a known token (USDC on Polygon)
        try:
            await self.geckoterminal.get_token_price(
                "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
                "polygon"
            )
            health['services']['geckoterminal'] = {"status": "healthy"}
        except Exception as e:
            health['services']['geckoterminal'] = {"status": "unhealthy", "error": str(e)}

        # Test DeFiLlama with same token
        try:
            await self.defillama.get_token_price(
                "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
                "polygon"
            )
            health['services']['defillama'] = {"status": "healthy"}
        except Exception as e:
            health['services']['defillama'] = {"status": "unhealthy", "error": str(e)}

        # Test Alchemy
        try:
            await self.alchemy.get_token_metadata("0x2791bca1f2de4661ed88a30c99a7a9449aa84174")
            health['services']['alchemy'] = {"status": "healthy"}
        except Exception as e:
            health['services']['alchemy'] = {"status": "unhealthy", "error": str(e)}

        health['overall'] = all(
            s.get('status') == 'healthy'
            for s in health['services'].values()
        )

        return health

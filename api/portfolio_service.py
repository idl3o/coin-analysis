"""
Portfolio Service for DDD Token Dashboard
Tracks all DDD pairs and provides aggregated data
"""
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import logging

from unified_price_service import UnifiedPriceService
from token_config import MAIN_TOKEN, QUOTE_TOKENS, LP_POOLS, PORTFOLIO

logger = logging.getLogger(__name__)


class PortfolioService:
    """
    Service for tracking the DDD token portfolio
    """

    def __init__(self):
        self.unified_price = UnifiedPriceService()
        self.main_token = MAIN_TOKEN
        self.quote_tokens = QUOTE_TOKENS
        self.lp_pools = LP_POOLS

    async def close(self):
        """Close all service connections"""
        await self.unified_price.close()

    async def get_main_token_data(self) -> Dict:
        """Get current data for the main DDD token"""
        try:
            data = await self.unified_price.get_token_price(
                self.main_token["contract"],
                self.main_token["network"]
            )
            return {
                "success": True,
                "symbol": self.main_token["symbol"],
                "data": data
            }
        except Exception as e:
            logger.error(f"Failed to get DDD token data: {str(e)}")
            return {
                "success": False,
                "symbol": self.main_token["symbol"],
                "error": str(e)
            }

    async def get_quote_token_data(self, token: Dict) -> Dict:
        """Get current data for a quote token"""
        try:
            data = await self.unified_price.get_token_price(
                token["contract"],
                token["network"]
            )
            return {
                "success": True,
                "symbol": token["symbol"],
                "pair": token["pair"],
                "contract": token["contract"],
                "data": data
            }
        except Exception as e:
            logger.warning(f"Failed to get {token['symbol']} data: {str(e)}")
            return {
                "success": False,
                "symbol": token["symbol"],
                "pair": token["pair"],
                "contract": token["contract"],
                "error": str(e)
            }

    async def get_all_quote_tokens(self) -> List[Dict]:
        """Get data for all quote tokens concurrently"""
        tasks = [self.get_quote_token_data(token) for token in self.quote_tokens]
        results = await asyncio.gather(*tasks)
        return results

    async def get_portfolio_summary(self) -> Dict:
        """
        Get complete portfolio summary including:
        - Main DDD token data
        - All quote token pairs
        - Success/failure stats
        - Total value metrics
        """
        # Get main token and all quote tokens concurrently
        main_task = self.get_main_token_data()
        quotes_task = self.get_all_quote_tokens()

        main_data, quote_data_list = await asyncio.gather(main_task, quotes_task)

        # Calculate statistics
        total_tokens = len(quote_data_list) + 1  # +1 for DDD
        successful = sum(1 for q in quote_data_list if q["success"]) + (1 if main_data["success"] else 0)
        failed = total_tokens - successful

        # Organize by success/failure
        successful_pairs = [q for q in quote_data_list if q["success"]]
        failed_pairs = [q for q in quote_data_list if not q["success"]]

        # Calculate total liquidity across all pairs
        total_liquidity = 0
        total_volume_24h = 0

        if main_data["success"]:
            main_price_data = main_data.get("data", {})
            total_liquidity += main_price_data.get("liquidity_usd", 0) or 0
            total_volume_24h += main_price_data.get("volume_24h", 0) or 0

        for pair in successful_pairs:
            if pair.get("data"):
                total_liquidity += pair["data"].get("liquidity_usd", 0) or 0
                total_volume_24h += pair["data"].get("volume_24h", 0) or 0

        return {
            "portfolio_name": PORTFOLIO["name"],
            "network": PORTFOLIO["network"],
            "timestamp": datetime.now().isoformat(),
            "main_token": main_data,
            "quote_tokens": {
                "successful": successful_pairs,
                "failed": failed_pairs,
                "total": len(quote_data_list)
            },
            "lp_pools": {
                "count": len(LP_POOLS),
                "pools": LP_POOLS,
                "note": "LP pools require separate handling via pool endpoints"
            },
            "statistics": {
                "total_tokens": total_tokens,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/total_tokens*100):.1f}%",
                "total_liquidity_usd": total_liquidity,
                "total_volume_24h_usd": total_volume_24h
            }
        }

    async def get_portfolio_prices_only(self) -> Dict:
        """
        Get simplified price data for all tokens (for quick dashboard updates)
        """
        main_data, quote_data_list = await asyncio.gather(
            self.get_main_token_data(),
            self.get_all_quote_tokens()
        )

        prices = {
            "timestamp": datetime.now().isoformat(),
            "main_token": {
                "symbol": self.main_token["symbol"],
                "price": main_data.get("data", {}).get("current_price") if main_data["success"] else None,
                "price_change_24h": main_data.get("data", {}).get("price_change_24h") if main_data["success"] else None
            },
            "pairs": []
        }

        for quote in quote_data_list:
            if quote["success"]:
                prices["pairs"].append({
                    "symbol": quote["symbol"],
                    "pair": quote["pair"],
                    "price": quote["data"].get("current_price"),
                    "price_change_24h": quote["data"].get("price_change_24h"),
                    "volume_24h": quote["data"].get("volume_24h"),
                    "source": quote["data"].get("source")
                })

        return prices

    async def get_token_with_historical(
        self,
        contract_address: str,
        days: int = 30
    ) -> Dict:
        """
        Get historical data for a specific token in the portfolio
        """
        try:
            data = await self.unified_price.get_token_with_historical(
                contract_address,
                self.main_token["network"],
                days
            )
            return {
                "success": True,
                "data": data
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_main_token_with_history(self, days: int = 30) -> Dict:
        """Get DDD token with historical data"""
        return await self.get_token_with_historical(
            self.main_token["contract"],
            days
        )

    async def get_top_pairs_by_liquidity(self, limit: int = 5) -> List[Dict]:
        """
        Get top N pairs by liquidity
        """
        quote_data_list = await self.get_all_quote_tokens()

        # Filter successful and extract liquidity
        pairs_with_liquidity = []
        for quote in quote_data_list:
            if quote["success"] and quote.get("data"):
                liquidity = quote["data"].get("liquidity_usd", 0) or 0
                pairs_with_liquidity.append({
                    "pair": quote["pair"],
                    "symbol": quote["symbol"],
                    "liquidity_usd": liquidity,
                    "price": quote["data"].get("current_price"),
                    "volume_24h": quote["data"].get("volume_24h", 0),
                    "source": quote["data"].get("source")
                })

        # Sort by liquidity
        pairs_with_liquidity.sort(key=lambda x: x["liquidity_usd"], reverse=True)

        return pairs_with_liquidity[:limit]

    async def get_top_pairs_by_volume(self, limit: int = 5) -> List[Dict]:
        """
        Get top N pairs by 24h volume
        """
        quote_data_list = await self.get_all_quote_tokens()

        # Filter successful and extract volume
        pairs_with_volume = []
        for quote in quote_data_list:
            if quote["success"] and quote.get("data"):
                volume = quote["data"].get("volume_24h", 0) or 0
                pairs_with_volume.append({
                    "pair": quote["pair"],
                    "symbol": quote["symbol"],
                    "volume_24h": volume,
                    "price": quote["data"].get("current_price"),
                    "liquidity_usd": quote["data"].get("liquidity_usd", 0),
                    "source": quote["data"].get("source")
                })

        # Sort by volume
        pairs_with_volume.sort(key=lambda x: x["volume_24h"], reverse=True)

        return pairs_with_volume[:limit]

    async def health_check(self) -> Dict:
        """
        Quick health check - test main token only
        """
        try:
            main_data = await self.get_main_token_data()
            return {
                "status": "healthy" if main_data["success"] else "degraded",
                "timestamp": datetime.now().isoformat(),
                "main_token_accessible": main_data["success"]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

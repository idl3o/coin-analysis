from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import from local api directory
from crypto_service import CryptoService
from technical_analysis import TechnicalAnalysis
from alchemy_service import AlchemyService
from unified_price_service import UnifiedPriceService
from geckoterminal_service import GeckoTerminalService
from defillama_service import DeFiLlamaService
from zapper_service import ZapperService
from portfolio_service import PortfolioService

app = FastAPI(title="Crypto Analysis API", version="1.0.0")

# CORS middleware - allow all origins for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Crypto Analysis API", "status": "running", "version": "1.0.0"}

@app.get("/crypto/price/{symbol}")
async def get_current_price(symbol: str):
    """Get current price for a cryptocurrency"""
    crypto_service = CryptoService()
    try:
        price_data = await crypto_service.get_current_price(symbol)
        return price_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await crypto_service.close()

@app.get("/crypto/prices")
async def get_multiple_prices(symbols: str = Query(..., description="Comma-separated symbols")):
    """Get current prices for multiple cryptocurrencies"""
    crypto_service = CryptoService()
    try:
        symbol_list = [s.strip() for s in symbols.split(",")]
        prices = await crypto_service.get_multiple_prices(symbol_list)
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await crypto_service.close()

@app.get("/crypto/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    days: int = Query(default=30, ge=1, le=365),
    interval: str = Query(default="daily", regex="^(hourly|daily)$")
):
    """Get historical price data for a cryptocurrency"""
    crypto_service = CryptoService()
    try:
        historical_data = await crypto_service.get_historical_data(symbol, days, interval)
        return historical_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await crypto_service.close()

@app.get("/crypto/indicators/{symbol}")
async def get_technical_indicators(
    symbol: str,
    days: int = Query(default=30, ge=1, le=365),
    interval: str = Query(default="daily", regex="^(hourly|daily)$")
):
    """Get technical analysis indicators for a cryptocurrency"""
    crypto_service = CryptoService()
    ta_service = TechnicalAnalysis()
    try:
        # Get historical data
        historical_data = await crypto_service.get_historical_data(symbol, days, interval)

        # Calculate indicators
        indicators = ta_service.calculate_all_indicators(historical_data)

        return {
            "symbol": symbol,
            "interval": interval,
            "indicators": indicators
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await crypto_service.close()

@app.get("/crypto/top")
async def get_top_cryptocurrencies(limit: int = Query(default=20, ge=1, le=100)):
    """Get top cryptocurrencies by market cap"""
    crypto_service = CryptoService()
    try:
        top_cryptos = await crypto_service.get_top_cryptocurrencies(limit)
        return top_cryptos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await crypto_service.close()

@app.get("/crypto/token/contract/{contract_address}")
async def get_token_by_contract(
    contract_address: str,
    platform: str = Query(default="polygon", description="Blockchain platform")
):
    """Get token data by contract address - tries CoinGecko first, falls back to Alchemy"""
    crypto_service = CryptoService()
    # Use platform to determine Alchemy network
    alchemy_service = AlchemyService(network=platform)

    try:
        # Try CoinGecko first
        token_data = await crypto_service.get_token_by_contract(contract_address, platform)
        return token_data
    except Exception as coingecko_error:
        # If CoinGecko fails, try Alchemy as fallback
        try:
            alchemy_data = await alchemy_service.get_token_metadata(contract_address)
            # Format to match expected structure
            return {
                "symbol": alchemy_data.get("symbol", ""),
                "name": alchemy_data.get("name", ""),
                "contract_address": contract_address,
                "platform": platform,
                "current_price": 0,  # Alchemy doesn't provide price
                "market_cap": None,
                "volume_24h": None,
                "price_change_24h": None,
                "price_change_percentage_24h": None,
                "image": alchemy_data.get("logo"),
                "coin_id": None,
                "last_updated": alchemy_data.get("last_updated"),
                "source": "alchemy"  # Indicate data source
            }
        except Exception as alchemy_error:
            raise HTTPException(
                status_code=500,
                detail=f"CoinGecko: {str(coingecko_error)}; Alchemy: {str(alchemy_error)}"
            )
    finally:
        await crypto_service.close()
        await alchemy_service.close()

@app.get("/crypto/token/{coin_id}/historical")
async def get_token_historical(
    coin_id: str,
    days: int = Query(default=30, ge=1, le=365)
):
    """Get historical data for a token by coin_id"""
    crypto_service = CryptoService()
    try:
        historical_data = await crypto_service.get_token_historical_data(coin_id, days)
        return historical_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await crypto_service.close()

@app.get("/crypto/token/{coin_id}/indicators")
async def get_token_indicators(
    coin_id: str,
    days: int = Query(default=30, ge=1, le=365)
):
    """Get technical indicators for a token by coin_id"""
    crypto_service = CryptoService()
    ta_service = TechnicalAnalysis()
    try:
        # Get historical data
        historical_data = await crypto_service.get_token_historical_data(coin_id, days)

        # Calculate indicators
        indicators = ta_service.calculate_all_indicators(historical_data)

        return {
            "coin_id": coin_id,
            "indicators": indicators
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await crypto_service.close()

@app.get("/crypto/token/alchemy/{contract_address}")
async def get_token_by_alchemy(contract_address: str):
    """Get token data using Alchemy API"""
    alchemy_service = AlchemyService()
    try:
        token_data = await alchemy_service.get_token_metadata(contract_address)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await alchemy_service.close()


# ============================================================================
# UNIFIED PRICE SERVICE ENDPOINTS (NEW - RECOMMENDED)
# ============================================================================

@app.get("/v2/token/{contract_address}")
async def get_token_unified(
    contract_address: str,
    network: str = Query(default="polygon", description="Network: ethereum, polygon, base, arbitrum, etc.")
):
    """
    Get token price with automatic fallback (GeckoTerminal → DeFiLlama → Alchemy).
    This is the RECOMMENDED endpoint for custom tokens.
    """
    unified_service = UnifiedPriceService()
    try:
        token_data = await unified_service.get_token_price(contract_address, network)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await unified_service.close()


@app.get("/v2/token/{contract_address}/historical")
async def get_token_unified_historical(
    contract_address: str,
    network: str = Query(default="polygon", description="Network: ethereum, polygon, base, arbitrum, etc."),
    days: int = Query(default=30, ge=1, le=365, description="Number of days of historical data")
):
    """
    Get token price with historical OHLCV data using unified service.
    Tries GeckoTerminal first, then DeFiLlama for historical data.
    """
    unified_service = UnifiedPriceService()
    try:
        token_data = await unified_service.get_token_with_historical(contract_address, network, days)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await unified_service.close()


@app.get("/v2/token/{contract_address}/indicators")
async def get_token_unified_indicators(
    contract_address: str,
    network: str = Query(default="polygon", description="Network: ethereum, polygon, base, arbitrum, etc."),
    days: int = Query(default=30, ge=1, le=365)
):
    """
    Get technical indicators for a custom token using unified service with historical data.
    """
    unified_service = UnifiedPriceService()
    ta_service = TechnicalAnalysis()
    try:
        # Get token with historical data
        token_data = await unified_service.get_token_with_historical(contract_address, network, days)

        # Extract historical data for indicators
        historical_data = {
            "symbol": token_data.get("symbol", ""),
            "data": token_data.get("historical_data", [])
        }

        # Calculate indicators
        indicators = ta_service.calculate_all_indicators(historical_data)

        return {
            "contract_address": contract_address,
            "network": network,
            "symbol": token_data.get("symbol", ""),
            "current_price": token_data.get("current_price"),
            "indicators": indicators,
            "source": token_data.get("source")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await unified_service.close()


@app.get("/v2/tokens/batch")
async def get_multiple_tokens_unified(
    contracts: str = Query(..., description="Comma-separated contract addresses"),
    networks: str = Query(..., description="Comma-separated networks (must match contracts order)")
):
    """
    Get prices for multiple custom tokens at once using unified service.
    Example: contracts=0xabc...,0xdef... networks=polygon,ethereum
    """
    unified_service = UnifiedPriceService()
    try:
        contract_list = [c.strip() for c in contracts.split(",")]
        network_list = [n.strip() for n in networks.split(",")]

        if len(contract_list) != len(network_list):
            raise HTTPException(
                status_code=400,
                detail="Number of contracts must match number of networks"
            )

        tokens = list(zip(contract_list, network_list))
        results = await unified_service.get_multiple_tokens(tokens)

        return {
            "count": len(results),
            "tokens": results
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await unified_service.close()


@app.get("/v2/token/{contract_address}/compare")
async def compare_price_sources(
    contract_address: str,
    network: str = Query(default="polygon", description="Network: ethereum, polygon, base, arbitrum, etc.")
):
    """
    Compare prices from all available sources (GeckoTerminal, DeFiLlama, Alchemy).
    Useful for debugging and validation.
    """
    unified_service = UnifiedPriceService()
    try:
        comparison = await unified_service.compare_sources(contract_address, network)
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await unified_service.close()


@app.get("/v2/health")
async def health_check_services():
    """
    Check health status of all price data services.
    """
    unified_service = UnifiedPriceService()
    try:
        health = await unified_service.health_check()
        return health
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await unified_service.close()


# ============================================================================
# DIRECT SERVICE ENDPOINTS (For specific use cases)
# ============================================================================

@app.get("/geckoterminal/token/{contract_address}")
async def get_token_geckoterminal(
    contract_address: str,
    network: str = Query(default="polygon", description="Network ID")
):
    """Get token data directly from GeckoTerminal"""
    gecko_service = GeckoTerminalService()
    try:
        token_data = await gecko_service.get_token_price(contract_address, network)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await gecko_service.close()


@app.get("/geckoterminal/search")
async def search_pools_geckoterminal(
    query: str = Query(..., description="Search query (token name or symbol)"),
    network: str = Query(None, description="Optional network filter")
):
    """Search for pools on GeckoTerminal"""
    gecko_service = GeckoTerminalService()
    try:
        results = await gecko_service.search_pools(query, network)
        return {"count": len(results), "pools": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await gecko_service.close()


@app.get("/defillama/token/{contract_address}")
async def get_token_defillama(
    contract_address: str,
    network: str = Query(default="polygon", description="Network: ethereum, polygon, etc.")
):
    """Get token data directly from DeFiLlama"""
    llama_service = DeFiLlamaService()
    try:
        token_data = await llama_service.get_token_price(contract_address, network)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await llama_service.close()


# ============================================================================
# PORTFOLIO ENDPOINTS (DDD Token Dashboard)
# ============================================================================

@app.get("/v2/portfolio/summary")
async def get_portfolio_summary():
    """
    Get complete DDD portfolio summary including:
    - Main DDD token data
    - All quote token pairs
    - LP pool information
    - Success/failure statistics
    - Total liquidity and volume
    """
    portfolio = PortfolioService()
    try:
        summary = await portfolio.get_portfolio_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await portfolio.close()


@app.get("/v2/portfolio/prices")
async def get_portfolio_prices():
    """
    Get simplified price data for all tokens (for quick dashboard updates).
    Returns only prices and 24h changes without full details.
    """
    portfolio = PortfolioService()
    try:
        prices = await portfolio.get_portfolio_prices_only()
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await portfolio.close()


@app.get("/v2/portfolio/ddd")
async def get_main_token():
    """
    Get detailed data for the main DDD token.
    """
    portfolio = PortfolioService()
    try:
        ddd_data = await portfolio.get_main_token_data()
        return ddd_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await portfolio.close()


@app.get("/v2/portfolio/ddd/historical")
async def get_main_token_historical(
    days: int = Query(default=30, ge=1, le=365, description="Number of days")
):
    """
    Get DDD token with historical OHLCV data.
    """
    portfolio = PortfolioService()
    try:
        data = await portfolio.get_main_token_with_history(days)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await portfolio.close()


@app.get("/v2/portfolio/pairs/top-liquidity")
async def get_top_pairs_liquidity(
    limit: int = Query(default=5, ge=1, le=20, description="Number of pairs to return")
):
    """
    Get top N trading pairs by liquidity.
    """
    portfolio = PortfolioService()
    try:
        top_pairs = await portfolio.get_top_pairs_by_liquidity(limit)
        return {
            "count": len(top_pairs),
            "pairs": top_pairs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await portfolio.close()


@app.get("/v2/portfolio/pairs/top-volume")
async def get_top_pairs_volume(
    limit: int = Query(default=5, ge=1, le=20, description="Number of pairs to return")
):
    """
    Get top N trading pairs by 24h volume.
    """
    portfolio = PortfolioService()
    try:
        top_pairs = await portfolio.get_top_pairs_by_volume(limit)
        return {
            "count": len(top_pairs),
            "pairs": top_pairs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await portfolio.close()


@app.get("/v2/portfolio/health")
async def portfolio_health():
    """
    Quick health check for portfolio tracking.
    """
    portfolio = PortfolioService()
    try:
        health = await portfolio.health_check()
        return health
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await portfolio.close()


# ============================================================================
# ZAPPER API ENDPOINTS
# ============================================================================

@app.get("/zapper/balances/{wallet_address}")
async def get_zapper_balances(
    wallet_address: str,
    network: str = Query(default="polygon", description="Network: ethereum, polygon, etc.")
):
    """
    Get token balances for a wallet using Zapper.
    """
    zapper = ZapperService()
    try:
        balances = await zapper.get_token_balances(wallet_address, network)
        return balances
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await zapper.close()


@app.get("/zapper/pool/{pool_address}")
async def get_zapper_pool_stats(
    pool_address: str,
    network: str = Query(default="polygon", description="Network"),
    dex: str = Query(default="uniswap-v2", description="DEX: uniswap-v2, sushiswap, quickswap, etc.")
):
    """
    Get liquidity pool statistics from Zapper.
    """
    zapper = ZapperService()
    try:
        stats = await zapper.get_pool_stats(pool_address, network, dex)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await zapper.close()


@app.get("/zapper/supported-dexes")
async def get_supported_dexes(
    network: str = Query(default="polygon", description="Network")
):
    """
    Get list of supported DEXes on a network.
    """
    zapper = ZapperService()
    try:
        dexes = await zapper.get_supported_dexes(network)
        return {
            "network": network,
            "dexes": dexes,
            "count": len(dexes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await zapper.close()


@app.get("/zapper/health")
async def zapper_health():
    """
    Check Zapper API health status.
    """
    zapper = ZapperService()
    try:
        health = await zapper.health_check()
        return health
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await zapper.close()


# Mangum handler for Vercel
handler = Mangum(app)

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

# Mangum handler for Vercel
handler = Mangum(app)

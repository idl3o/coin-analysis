from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta

from services.crypto_service import CryptoService
from services.technical_analysis import TechnicalAnalysis
from models.schemas import CryptoPrice, TechnicalIndicators, HistoricalData

crypto_router = APIRouter()
crypto_service = CryptoService()
ta_service = TechnicalAnalysis()

@crypto_router.get("/price/{symbol}")
async def get_current_price(symbol: str):
    """Get current price for a cryptocurrency"""
    try:
        price_data = await crypto_service.get_current_price(symbol)
        return price_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@crypto_router.get("/prices")
async def get_multiple_prices(symbols: str = Query(..., description="Comma-separated symbols")):
    """Get current prices for multiple cryptocurrencies"""
    try:
        symbol_list = [s.strip() for s in symbols.split(",")]
        prices = await crypto_service.get_multiple_prices(symbol_list)
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@crypto_router.get("/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    days: int = Query(default=30, ge=1, le=365),
    interval: str = Query(default="daily", regex="^(hourly|daily)$")
):
    """Get historical price data for a cryptocurrency"""
    try:
        historical_data = await crypto_service.get_historical_data(symbol, days, interval)
        return historical_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@crypto_router.get("/indicators/{symbol}")
async def get_technical_indicators(
    symbol: str,
    days: int = Query(default=30, ge=1, le=365),
    interval: str = Query(default="daily", regex="^(hourly|daily)$")
):
    """Get technical analysis indicators for a cryptocurrency"""
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

@crypto_router.get("/top")
async def get_top_cryptocurrencies(limit: int = Query(default=20, ge=1, le=100)):
    """Get top cryptocurrencies by market cap"""
    try:
        top_cryptos = await crypto_service.get_top_cryptocurrencies(limit)
        return top_cryptos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@crypto_router.get("/token/contract/{contract_address}")
async def get_token_by_contract(
    contract_address: str,
    platform: str = Query(default="ethereum", description="Blockchain platform (ethereum, binance-smart-chain, etc.)")
):
    """Get token data by contract address"""
    try:
        token_data = await crypto_service.get_token_by_contract(contract_address, platform)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@crypto_router.get("/token/{coin_id}/historical")
async def get_token_historical(
    coin_id: str,
    days: int = Query(default=30, ge=1, le=365)
):
    """Get historical data for a token by coin_id"""
    try:
        historical_data = await crypto_service.get_token_historical_data(coin_id, days)
        return historical_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@crypto_router.get("/token/{coin_id}/indicators")
async def get_token_indicators(
    coin_id: str,
    days: int = Query(default=30, ge=1, le=365)
):
    """Get technical indicators for a token by coin_id"""
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

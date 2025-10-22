from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class CryptoPrice(BaseModel):
    symbol: str
    name: str
    current_price: float
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None
    last_updated: datetime

class HistoricalDataPoint(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

class HistoricalData(BaseModel):
    symbol: str
    data: List[HistoricalDataPoint]

class MovingAverages(BaseModel):
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None

class RSI(BaseModel):
    value: Optional[float] = None
    signal: str = "neutral"  # overbought, oversold, neutral

class MACD(BaseModel):
    macd_line: Optional[float] = None
    signal_line: Optional[float] = None
    histogram: Optional[float] = None
    signal: str = "neutral"  # bullish, bearish, neutral

class BollingerBands(BaseModel):
    upper: Optional[float] = None
    middle: Optional[float] = None
    lower: Optional[float] = None
    bandwidth: Optional[float] = None

class TechnicalIndicators(BaseModel):
    current_price: float
    moving_averages: MovingAverages
    rsi: RSI
    macd: MACD
    bollinger_bands: BollingerBands
    volume_trend: str = "neutral"
    overall_signal: str = "neutral"

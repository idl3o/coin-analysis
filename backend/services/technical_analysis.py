from typing import Dict, List
import statistics

class TechnicalAnalysis:
    def __init__(self):
        pass

    def _get_closes(self, historical_data: Dict) -> List[float]:
        """Extract close prices from historical data"""
        return [float(candle['close']) for candle in historical_data['data']]

    def calculate_sma(self, values: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(values) < period:
            return None
        return sum(values[-period:]) / period

    def calculate_ema(self, values: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        if len(values) < period:
            return None

        multiplier = 2 / (period + 1)
        ema = sum(values[:period]) / period  # Start with SMA

        for price in values[period:]:
            ema = (price - ema) * multiplier + ema

        return ema

    def calculate_moving_averages(self, closes: List[float]) -> Dict:
        """Calculate various moving averages"""
        return {
            "sma_20": self.calculate_sma(closes, 20),
            "sma_50": self.calculate_sma(closes, 50),
            "sma_200": self.calculate_sma(closes, 200),
            "ema_12": self.calculate_ema(closes, 12),
            "ema_26": self.calculate_ema(closes, 26),
        }

    def calculate_rsi(self, closes: List[float], period: int = 14) -> Dict:
        """Calculate RSI indicator"""
        if len(closes) < period + 1:
            return {"value": None, "signal": "neutral"}

        changes = [closes[i] - closes[i-1] for i in range(1, len(closes))]

        gains = [change if change > 0 else 0 for change in changes]
        losses = [abs(change) if change < 0 else 0 for change in changes]

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            rsi_value = 100
        else:
            rs = avg_gain / avg_loss
            rsi_value = 100 - (100 / (1 + rs))

        # Determine signal
        if rsi_value > 70:
            signal = "overbought"
        elif rsi_value < 30:
            signal = "oversold"
        else:
            signal = "neutral"

        return {
            "value": round(rsi_value, 2),
            "signal": signal
        }

    def calculate_macd(self, closes: List[float]) -> Dict:
        """Calculate MACD indicator"""
        if len(closes) < 26:
            return {
                "macd_line": None,
                "signal_line": None,
                "histogram": None,
                "signal": "neutral"
            }

        ema_12 = self.calculate_ema(closes, 12)
        ema_26 = self.calculate_ema(closes, 26)

        if ema_12 is None or ema_26 is None:
            return {
                "macd_line": None,
                "signal_line": None,
                "histogram": None,
                "signal": "neutral"
            }

        macd_line = ema_12 - ema_26

        # Calculate signal line (9-period EMA of MACD)
        macd_values = []
        for i in range(26, len(closes) + 1):
            ema12 = self.calculate_ema(closes[:i], 12)
            ema26 = self.calculate_ema(closes[:i], 26)
            if ema12 and ema26:
                macd_values.append(ema12 - ema26)

        signal_line = self.calculate_ema(macd_values, 9) if len(macd_values) >= 9 else macd_line
        histogram = macd_line - signal_line if signal_line else 0

        # Determine signal
        if macd_line > signal_line and histogram > 0:
            signal = "bullish"
        elif macd_line < signal_line and histogram < 0:
            signal = "bearish"
        else:
            signal = "neutral"

        return {
            "macd_line": round(macd_line, 2),
            "signal_line": round(signal_line, 2) if signal_line else None,
            "histogram": round(histogram, 2),
            "signal": signal
        }

    def calculate_bollinger_bands(self, closes: List[float], period: int = 20) -> Dict:
        """Calculate Bollinger Bands"""
        if len(closes) < period:
            return {
                "upper": None,
                "middle": None,
                "lower": None,
                "bandwidth": None
            }

        sma = self.calculate_sma(closes, period)
        recent_closes = closes[-period:]

        # Calculate standard deviation
        variance = sum((x - sma) ** 2 for x in recent_closes) / period
        std_dev = variance ** 0.5

        upper = sma + (2 * std_dev)
        lower = sma - (2 * std_dev)
        bandwidth = (upper - lower) / sma if sma != 0 else 0

        return {
            "upper": round(upper, 2),
            "middle": round(sma, 2),
            "lower": round(lower, 2),
            "bandwidth": round(bandwidth, 4)
        }

    def analyze_volume_trend(self, historical_data: Dict) -> str:
        """Analyze volume trend (if available)"""
        volumes = [candle.get('volume', 0) for candle in historical_data['data']]

        if sum(volumes) == 0 or len(volumes) < 20:
            return "neutral"

        recent_volume = sum(volumes[-5:]) / 5
        older_volume = sum(volumes[-20:-5]) / 15

        if older_volume == 0:
            return "neutral"

        if recent_volume > older_volume * 1.2:
            return "increasing"
        elif recent_volume < older_volume * 0.8:
            return "decreasing"
        else:
            return "neutral"

    def calculate_overall_signal(self, indicators: Dict) -> str:
        """Calculate overall trading signal based on all indicators"""
        signals = []

        # RSI signal
        if indicators["rsi"]["value"]:
            if indicators["rsi"]["signal"] == "oversold":
                signals.append(1)  # Bullish
            elif indicators["rsi"]["signal"] == "overbought":
                signals.append(-1)  # Bearish

        # MACD signal
        if indicators["macd"]["signal"] == "bullish":
            signals.append(1)
        elif indicators["macd"]["signal"] == "bearish":
            signals.append(-1)

        # Moving average crossover
        ma = indicators["moving_averages"]
        if ma["ema_12"] and ma["ema_26"]:
            if ma["ema_12"] > ma["ema_26"]:
                signals.append(1)
            else:
                signals.append(-1)

        # Calculate average
        if not signals:
            return "neutral"

        avg_signal = sum(signals) / len(signals)

        if avg_signal > 0.3:
            return "bullish"
        elif avg_signal < -0.3:
            return "bearish"
        else:
            return "neutral"

    def calculate_all_indicators(self, historical_data: Dict) -> Dict:
        """Calculate all technical indicators"""
        closes = self._get_closes(historical_data)

        if not closes:
            return {
                "current_price": 0,
                "moving_averages": {},
                "rsi": {"value": None, "signal": "neutral"},
                "macd": {},
                "bollinger_bands": {},
                "volume_trend": "neutral",
                "overall_signal": "neutral"
            }

        current_price = closes[-1]
        moving_averages = self.calculate_moving_averages(closes)
        rsi = self.calculate_rsi(closes)
        macd = self.calculate_macd(closes)
        bollinger_bands = self.calculate_bollinger_bands(closes)
        volume_trend = self.analyze_volume_trend(historical_data)

        indicators = {
            "current_price": current_price,
            "moving_averages": moving_averages,
            "rsi": rsi,
            "macd": macd,
            "bollinger_bands": bollinger_bands,
            "volume_trend": volume_trend
        }

        indicators["overall_signal"] = self.calculate_overall_signal(indicators)

        return indicators

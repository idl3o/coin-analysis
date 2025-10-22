import pandas as pd
import pandas_ta as ta
from typing import Dict, List

class TechnicalAnalysis:
    def __init__(self):
        pass

    def _prepare_dataframe(self, historical_data: Dict) -> pd.DataFrame:
        """Convert historical data to pandas DataFrame"""
        df = pd.DataFrame(historical_data["data"])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('datetime', inplace=True)
        df = df.sort_index()
        return df

    def calculate_moving_averages(self, df: pd.DataFrame) -> Dict:
        """Calculate various moving averages"""
        close = df['close']

        return {
            "sma_20": float(ta.sma(close, length=20).iloc[-1]) if len(df) >= 20 else None,
            "sma_50": float(ta.sma(close, length=50).iloc[-1]) if len(df) >= 50 else None,
            "sma_200": float(ta.sma(close, length=200).iloc[-1]) if len(df) >= 200 else None,
            "ema_12": float(ta.ema(close, length=12).iloc[-1]) if len(df) >= 12 else None,
            "ema_26": float(ta.ema(close, length=26).iloc[-1]) if len(df) >= 26 else None,
        }

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> Dict:
        """Calculate RSI indicator"""
        if len(df) < period:
            return {"value": None, "signal": "neutral"}

        rsi = ta.rsi(df['close'], length=period)
        rsi_value = float(rsi.iloc[-1])

        # Determine signal
        if rsi_value > 70:
            signal = "overbought"
        elif rsi_value < 30:
            signal = "oversold"
        else:
            signal = "neutral"

        return {
            "value": rsi_value,
            "signal": signal
        }

    def calculate_macd(self, df: pd.DataFrame) -> Dict:
        """Calculate MACD indicator"""
        if len(df) < 26:
            return {
                "macd_line": None,
                "signal_line": None,
                "histogram": None,
                "signal": "neutral"
            }

        macd_result = ta.macd(df['close'])

        if macd_result is None or macd_result.empty:
            return {
                "macd_line": None,
                "signal_line": None,
                "histogram": None,
                "signal": "neutral"
            }

        macd_line = float(macd_result['MACD_12_26_9'].iloc[-1])
        signal_line = float(macd_result['MACDs_12_26_9'].iloc[-1])
        histogram = float(macd_result['MACDh_12_26_9'].iloc[-1])

        # Determine signal
        if macd_line > signal_line and histogram > 0:
            signal = "bullish"
        elif macd_line < signal_line and histogram < 0:
            signal = "bearish"
        else:
            signal = "neutral"

        return {
            "macd_line": macd_line,
            "signal_line": signal_line,
            "histogram": histogram,
            "signal": signal
        }

    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20) -> Dict:
        """Calculate Bollinger Bands"""
        if len(df) < period:
            return {
                "upper": None,
                "middle": None,
                "lower": None,
                "bandwidth": None
            }

        bbands = ta.bbands(df['close'], length=period)

        if bbands is None or bbands.empty:
            return {
                "upper": None,
                "middle": None,
                "lower": None,
                "bandwidth": None
            }

        upper = float(bbands[f'BBU_{period}_2.0'].iloc[-1])
        middle = float(bbands[f'BBM_{period}_2.0'].iloc[-1])
        lower = float(bbands[f'BBL_{period}_2.0'].iloc[-1])
        bandwidth = float(bbands[f'BBB_{period}_2.0'].iloc[-1])

        return {
            "upper": upper,
            "middle": middle,
            "lower": lower,
            "bandwidth": bandwidth
        }

    def analyze_volume_trend(self, df: pd.DataFrame) -> str:
        """Analyze volume trend (if available)"""
        if 'volume' not in df.columns or df['volume'].sum() == 0:
            return "neutral"

        recent_volume = df['volume'].tail(5).mean()
        older_volume = df['volume'].tail(20).head(15).mean()

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
        df = self._prepare_dataframe(historical_data)

        current_price = float(df['close'].iloc[-1])
        moving_averages = self.calculate_moving_averages(df)
        rsi = self.calculate_rsi(df)
        macd = self.calculate_macd(df)
        bollinger_bands = self.calculate_bollinger_bands(df)
        volume_trend = self.analyze_volume_trend(df)

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

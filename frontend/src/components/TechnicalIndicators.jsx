import { TrendingUp, TrendingDown, Activity, BarChart3, AlertCircle } from 'lucide-react'
import './TechnicalIndicators.css'

function TechnicalIndicators({ symbol, indicators }) {
  if (!indicators || !indicators.indicators) {
    return <div className="technical-indicators">No indicators available</div>
  }

  const ind = indicators.indicators
  const overallSignal = ind.overall_signal || 'neutral'

  const getSignalColor = (signal) => {
    if (signal === 'bullish' || signal === 'oversold') return 'positive'
    if (signal === 'bearish' || signal === 'overbought') return 'negative'
    return 'neutral'
  }

  const getSignalIcon = (signal) => {
    if (signal === 'bullish' || signal === 'oversold') return <TrendingUp size={20} />
    if (signal === 'bearish' || signal === 'overbought') return <TrendingDown size={20} />
    return <Activity size={20} />
  }

  return (
    <div className="technical-indicators">
      <h2>Technical Analysis</h2>

      <div className={`overall-signal ${getSignalColor(overallSignal)}`}>
        {getSignalIcon(overallSignal)}
        <div>
          <span className="signal-label">Overall Signal</span>
          <span className="signal-value">{overallSignal.toUpperCase()}</span>
        </div>
      </div>

      <div className="indicators-list">
        {/* RSI */}
        <div className="indicator-card">
          <div className="indicator-header">
            <Activity size={18} />
            <h3>RSI (14)</h3>
          </div>
          {ind.rsi?.value ? (
            <>
              <div className="indicator-value-large">
                {ind.rsi.value.toFixed(2)}
              </div>
              <div className={`indicator-signal ${getSignalColor(ind.rsi.signal)}`}>
                {ind.rsi.signal.toUpperCase()}
              </div>
              <div className="rsi-bar">
                <div
                  className="rsi-fill"
                  style={{ width: `${ind.rsi.value}%` }}
                />
                <div className="rsi-marker oversold" style={{ left: '30%' }} />
                <div className="rsi-marker overbought" style={{ left: '70%' }} />
              </div>
            </>
          ) : (
            <div className="no-data">Insufficient data</div>
          )}
        </div>

        {/* MACD */}
        <div className="indicator-card">
          <div className="indicator-header">
            <BarChart3 size={18} />
            <h3>MACD</h3>
          </div>
          {ind.macd?.macd_line !== null ? (
            <>
              <div className="macd-values">
                <div className="macd-item">
                  <span className="macd-label">MACD:</span>
                  <span className="macd-value">{ind.macd.macd_line?.toFixed(2)}</span>
                </div>
                <div className="macd-item">
                  <span className="macd-label">Signal:</span>
                  <span className="macd-value">{ind.macd.signal_line?.toFixed(2)}</span>
                </div>
                <div className="macd-item">
                  <span className="macd-label">Histogram:</span>
                  <span className={`macd-value ${ind.macd.histogram >= 0 ? 'positive' : 'negative'}`}>
                    {ind.macd.histogram?.toFixed(2)}
                  </span>
                </div>
              </div>
              <div className={`indicator-signal ${getSignalColor(ind.macd.signal)}`}>
                {ind.macd.signal.toUpperCase()}
              </div>
            </>
          ) : (
            <div className="no-data">Insufficient data</div>
          )}
        </div>

        {/* Moving Averages */}
        <div className="indicator-card">
          <div className="indicator-header">
            <TrendingUp size={18} />
            <h3>Moving Averages</h3>
          </div>
          <div className="ma-list">
            {ind.moving_averages?.sma_20 && (
              <div className="ma-item">
                <span className="ma-label">SMA 20:</span>
                <span className="ma-value">${ind.moving_averages.sma_20.toFixed(2)}</span>
              </div>
            )}
            {ind.moving_averages?.sma_50 && (
              <div className="ma-item">
                <span className="ma-label">SMA 50:</span>
                <span className="ma-value">${ind.moving_averages.sma_50.toFixed(2)}</span>
              </div>
            )}
            {ind.moving_averages?.ema_12 && (
              <div className="ma-item">
                <span className="ma-label">EMA 12:</span>
                <span className="ma-value">${ind.moving_averages.ema_12.toFixed(2)}</span>
              </div>
            )}
            {ind.moving_averages?.ema_26 && (
              <div className="ma-item">
                <span className="ma-label">EMA 26:</span>
                <span className="ma-value">${ind.moving_averages.ema_26.toFixed(2)}</span>
              </div>
            )}
          </div>
        </div>

        {/* Bollinger Bands */}
        <div className="indicator-card">
          <div className="indicator-header">
            <AlertCircle size={18} />
            <h3>Bollinger Bands</h3>
          </div>
          {ind.bollinger_bands?.upper ? (
            <div className="bb-list">
              <div className="bb-item">
                <span className="bb-label">Upper:</span>
                <span className="bb-value">${ind.bollinger_bands.upper.toFixed(2)}</span>
              </div>
              <div className="bb-item">
                <span className="bb-label">Middle:</span>
                <span className="bb-value">${ind.bollinger_bands.middle.toFixed(2)}</span>
              </div>
              <div className="bb-item">
                <span className="bb-label">Lower:</span>
                <span className="bb-value">${ind.bollinger_bands.lower.toFixed(2)}</span>
              </div>
              <div className="bb-item">
                <span className="bb-label">Bandwidth:</span>
                <span className="bb-value">{ind.bollinger_bands.bandwidth?.toFixed(4)}</span>
              </div>
            </div>
          ) : (
            <div className="no-data">Insufficient data</div>
          )}
        </div>

        {/* Volume Trend */}
        <div className="indicator-card">
          <div className="indicator-header">
            <BarChart3 size={18} />
            <h3>Volume Trend</h3>
          </div>
          <div className={`indicator-signal ${ind.volume_trend === 'increasing' ? 'positive' : ind.volume_trend === 'decreasing' ? 'negative' : 'neutral'}`}>
            {ind.volume_trend.toUpperCase()}
          </div>
        </div>
      </div>
    </div>
  )
}

export default TechnicalIndicators

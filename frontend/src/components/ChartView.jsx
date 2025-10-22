import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts'
import './ChartView.css'

function ChartView({ symbol, historicalData, indicators }) {
  if (!historicalData || !historicalData.data || historicalData.data.length === 0) {
    return <div className="chart-view">No data available</div>
  }

  // Prepare chart data
  const chartData = historicalData.data.map((point) => ({
    date: new Date(point.timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    }),
    price: point.close,
    high: point.high,
    low: point.low,
    timestamp: point.timestamp
  }))

  const currentPrice = indicators?.indicators?.current_price || chartData[chartData.length - 1]?.price

  const formatPrice = (value) => {
    return `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
  }

  // Get moving average values if available
  const ma20 = indicators?.indicators?.moving_averages?.sma_20
  const ma50 = indicators?.indicators?.moving_averages?.sma_50

  return (
    <div className="chart-view">
      <div className="chart-header">
        <h2>{symbol} Price Chart</h2>
        <div className="current-price-display">
          <span className="current-price-label">Current Price:</span>
          <span className="current-price-value">{formatPrice(currentPrice)}</span>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="date"
            stroke="#666"
            tick={{ fontSize: 12 }}
          />
          <YAxis
            stroke="#666"
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => `$${value.toLocaleString()}`}
            domain={['auto', 'auto']}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '10px'
            }}
            formatter={(value, name) => {
              if (name === 'price') return [formatPrice(value), 'Price']
              if (name === 'high') return [formatPrice(value), 'High']
              if (name === 'low') return [formatPrice(value), 'Low']
              return [value, name]
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#667eea"
            strokeWidth={2}
            dot={false}
            name="Price"
          />
          {ma20 && (
            <ReferenceLine
              y={ma20}
              stroke="#10b981"
              strokeDasharray="5 5"
              label={{ value: 'MA20', position: 'right', fill: '#10b981', fontSize: 12 }}
            />
          )}
          {ma50 && (
            <ReferenceLine
              y={ma50}
              stroke="#f59e0b"
              strokeDasharray="5 5"
              label={{ value: 'MA50', position: 'right', fill: '#f59e0b', fontSize: 12 }}
            />
          )}
        </LineChart>
      </ResponsiveContainer>

      <div className="price-range">
        <div className="range-item">
          <span className="label">High:</span>
          <span className="value">{formatPrice(Math.max(...chartData.map(d => d.high)))}</span>
        </div>
        <div className="range-item">
          <span className="label">Low:</span>
          <span className="value">{formatPrice(Math.min(...chartData.map(d => d.low)))}</span>
        </div>
        <div className="range-item">
          <span className="label">Avg:</span>
          <span className="value">
            {formatPrice(chartData.reduce((sum, d) => sum + d.price, 0) / chartData.length)}
          </span>
        </div>
      </div>
    </div>
  )
}

export default ChartView

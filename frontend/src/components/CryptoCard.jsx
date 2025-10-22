import { TrendingUp, TrendingDown } from 'lucide-react'
import './CryptoCard.css'

function CryptoCard({ crypto, isSelected, onClick }) {
  const isPositive = crypto.price_change_percentage_24h >= 0

  return (
    <div
      className={`crypto-card ${isSelected ? 'selected' : ''}`}
      onClick={onClick}
    >
      <div className="card-header">
        {crypto.image && (
          <img src={crypto.image} alt={crypto.name} className="card-icon" />
        )}
        <div className="card-title">
          <h3>{crypto.symbol}</h3>
          <p className="card-name">{crypto.name}</p>
        </div>
      </div>

      <div className="card-price">
        <span className="price">${crypto.current_price?.toLocaleString()}</span>
        <div className={`change-badge ${isPositive ? 'positive' : 'negative'}`}>
          {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
          <span>{Math.abs(crypto.price_change_percentage_24h).toFixed(2)}%</span>
        </div>
      </div>

      <div className="card-stats">
        <div className="stat">
          <span className="stat-label">Market Cap</span>
          <span className="stat-value">
            ${(crypto.market_cap / 1e9).toFixed(2)}B
          </span>
        </div>
        <div className="stat">
          <span className="stat-label">Volume 24h</span>
          <span className="stat-value">
            ${(crypto.volume_24h / 1e6).toFixed(0)}M
          </span>
        </div>
      </div>
    </div>
  )
}

export default CryptoCard

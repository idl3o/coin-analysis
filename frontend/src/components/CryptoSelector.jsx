import './CryptoSelector.css'

function CryptoSelector({ cryptos, selectedSymbol, onSelectSymbol }) {
  return (
    <div className="crypto-selector">
      <h2>Select Cryptocurrency</h2>
      <div className="selector-buttons">
        {cryptos.map((crypto) => (
          <button
            key={crypto.symbol}
            className={`crypto-button ${crypto.symbol === selectedSymbol ? 'active' : ''}`}
            onClick={() => onSelectSymbol(crypto.symbol)}
          >
            {crypto.image && (
              <img src={crypto.image} alt={crypto.name} className="crypto-icon" />
            )}
            <div className="crypto-info">
              <span className="symbol">{crypto.symbol}</span>
              <span className="name">{crypto.name}</span>
            </div>
            <div className="price-info">
              <span className="price">${crypto.current_price?.toLocaleString()}</span>
              <span className={`change ${crypto.price_change_percentage_24h >= 0 ? 'positive' : 'negative'}`}>
                {crypto.price_change_percentage_24h?.toFixed(2)}%
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

export default CryptoSelector

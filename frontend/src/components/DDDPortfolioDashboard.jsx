import { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Activity, DollarSign, BarChart3, RefreshCw } from 'lucide-react';
import { cryptoAPI } from '../services/api';
import { MAIN_TOKEN, LP_POOLS } from '../config/customTokens';
import './DDDPortfolioDashboard.css';

export default function DDDPortfolioDashboard() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [refreshing, setRefreshing] = useState(false);

  const fetchPortfolio = async () => {
    try {
      setRefreshing(true);
      const data = await cryptoAPI.getPortfolioSummary();
      setPortfolio(data);
      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      console.error('Error fetching portfolio:', err);
      setError(err.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchPortfolio();

    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchPortfolio, 30000);
    return () => clearInterval(interval);
  }, []);

  const formatPrice = (price) => {
    if (!price) return 'N/A';
    return price < 0.01 ? price.toFixed(8) : price.toFixed(6);
  };

  const formatVolume = (volume) => {
    if (!volume) return 'N/A';
    if (volume >= 1000000) return `$${(volume / 1000000).toFixed(2)}M`;
    if (volume >= 1000) return `$${(volume / 1000).toFixed(2)}K`;
    return `$${volume.toFixed(2)}`;
  };

  const getPriceChangeColor = (change) => {
    if (!change) return 'neutral';
    return change >= 0 ? 'positive' : 'negative';
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading DDD Portfolio...</p>
      </div>
    );
  }

  if (error && !portfolio) {
    return (
      <div className="error-container">
        <p>Error loading portfolio: {error}</p>
        <button onClick={fetchPortfolio} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  const mainTokenData = portfolio?.main_token;
  const successfulPairs = portfolio?.quote_tokens?.successful || [];
  const failedPairs = portfolio?.quote_tokens?.failed || [];
  const stats = portfolio?.statistics || {};

  return (
    <div className="ddd-portfolio-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>DDD Token Dashboard</h1>
          <p className="subtitle">Durgan Dynasty Doubloon Portfolio</p>
        </div>
        <div className="header-actions">
          <div className="last-updated">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </div>
          <button
            onClick={fetchPortfolio}
            className={`refresh-button ${refreshing ? 'refreshing' : ''}`}
            disabled={refreshing}
          >
            <RefreshCw size={16} />
            {refreshing ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
      </header>

      {/* Main DDD Token Section */}
      <section className="main-token-section">
        <h2 className="section-title">
          <Activity size={20} />
          Main Token
        </h2>

        {mainTokenData?.success ? (
          <div className="main-token-card">
            <div className="token-header">
              <div className="token-info">
                <h3>{mainTokenData.data.name || 'DDD Token'}</h3>
                <span className="token-symbol">{mainTokenData.data.symbol || 'DDD'}</span>
                <span className="token-network">Polygon</span>
              </div>
              <div className="token-source">
                <span className="source-badge">{mainTokenData.data.source}</span>
              </div>
            </div>

            <div className="price-display">
              <div className="current-price">
                <span className="price-label">Price</span>
                <span className="price-value">
                  ${formatPrice(mainTokenData.data.current_price)}
                </span>
              </div>
              {mainTokenData.data.price_change_24h !== null && (
                <div className={`price-change ${getPriceChangeColor(mainTokenData.data.price_change_24h)}`}>
                  {mainTokenData.data.price_change_24h >= 0 ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                  {Math.abs(mainTokenData.data.price_change_24h).toFixed(2)}%
                </div>
              )}
            </div>

            <div className="token-stats">
              <div className="stat-item">
                <div className="stat-icon">
                  <BarChart3 size={16} />
                </div>
                <div className="stat-content">
                  <span className="stat-label">24h Volume</span>
                  <span className="stat-value">{formatVolume(mainTokenData.data.volume_24h)}</span>
                </div>
              </div>
              <div className="stat-item">
                <div className="stat-icon">
                  <DollarSign size={16} />
                </div>
                <div className="stat-content">
                  <span className="stat-label">Liquidity</span>
                  <span className="stat-value">{formatVolume(mainTokenData.data.liquidity_usd)}</span>
                </div>
              </div>
            </div>

            <div className="token-address">
              <span className="address-label">Contract:</span>
              <code>{MAIN_TOKEN.contractAddress.slice(0, 10)}...{MAIN_TOKEN.contractAddress.slice(-8)}</code>
            </div>
          </div>
        ) : (
          <div className="error-card">
            <p>Unable to load DDD token data</p>
            <small>{mainTokenData?.error}</small>
          </div>
        )}
      </section>

      {/* Portfolio Statistics */}
      <section className="stats-section">
        <h2 className="section-title">
          <BarChart3 size={20} />
          Portfolio Overview
        </h2>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-card-label">Total Tokens</div>
            <div className="stat-card-value">{stats.total_tokens || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-label">Successfully Tracked</div>
            <div className="stat-card-value success">{stats.successful || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-label">Success Rate</div>
            <div className="stat-card-value">{stats.success_rate || '0%'}</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-label">Total Liquidity</div>
            <div className="stat-card-value">{formatVolume(stats.total_liquidity_usd)}</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-label">Total Volume (24h)</div>
            <div className="stat-card-value">{formatVolume(stats.total_volume_24h_usd)}</div>
          </div>
        </div>
      </section>

      {/* Trading Pairs */}
      <section className="pairs-section">
        <h2 className="section-title">
          <TrendingUp size={20} />
          Trading Pairs ({successfulPairs.length} Active)
        </h2>

        {successfulPairs.length > 0 ? (
          <div className="pairs-grid">
            {successfulPairs.map((pair, idx) => (
              <div key={idx} className="pair-card">
                <div className="pair-header">
                  <h4>{pair.pair}</h4>
                  <span className="pair-symbol">{pair.symbol}</span>
                </div>
                <div className="pair-price">
                  ${formatPrice(pair.data.current_price)}
                </div>
                {pair.data.price_change_24h !== null && (
                  <div className={`pair-change ${getPriceChangeColor(pair.data.price_change_24h)}`}>
                    {pair.data.price_change_24h >= 0 ? '↑' : '↓'} {Math.abs(pair.data.price_change_24h).toFixed(2)}%
                  </div>
                )}
                <div className="pair-stats">
                  <div className="pair-stat">
                    <span>Volume:</span>
                    <span>{formatVolume(pair.data.volume_24h)}</span>
                  </div>
                  <div className="pair-stat">
                    <span>Liquidity:</span>
                    <span>{formatVolume(pair.data.liquidity_usd)}</span>
                  </div>
                </div>
                <div className="pair-source">
                  <span className="source-tag">{pair.data.source}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No trading pairs are currently being tracked by APIs.</p>
            <small>These tokens may be too new or have low liquidity.</small>
          </div>
        )}

        {failedPairs.length > 0 && (
          <div className="failed-pairs">
            <details>
              <summary>Untracked Pairs ({failedPairs.length})</summary>
              <div className="failed-pairs-list">
                {failedPairs.map((pair, idx) => (
                  <div key={idx} className="failed-pair-item">
                    <span>{pair.pair}</span>
                    <span className="failed-badge">Not indexed</span>
                  </div>
                ))}
              </div>
            </details>
          </div>
        )}
      </section>

      {/* LP Pools */}
      {LP_POOLS.length > 0 && (
        <section className="pools-section">
          <h2 className="section-title">
            <DollarSign size={20} />
            Liquidity Pool Positions ({LP_POOLS.length})
          </h2>
          <div className="pools-list">
            {LP_POOLS.map((pool, idx) => (
              <div key={idx} className="pool-card">
                <div className="pool-info">
                  <h4>{pool.pair}</h4>
                  <span className="pool-type">LP Token</span>
                </div>
                <div className="pool-address">
                  <code>{pool.poolAddress.slice(0, 16)}...{pool.poolAddress.slice(-8)}</code>
                </div>
                <div className="pool-note">
                  <small>Requires pool contract query for pricing</small>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>
          Powered by GeckoTerminal, DeFiLlama, and Alchemy •
          Auto-refreshes every 30 seconds •
          All prices in USD
        </p>
      </footer>
    </div>
  );
}

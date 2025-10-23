import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const cryptoAPI = {
  // ============================================================================
  // DDD PORTFOLIO ENDPOINTS (NEW)
  // ============================================================================

  // Get complete DDD portfolio summary
  getPortfolioSummary: async () => {
    const response = await axios.get(`${API_BASE_URL}/v2/portfolio/summary`);
    return response.data;
  },

  // Get quick price updates for portfolio
  getPortfolioPrices: async () => {
    const response = await axios.get(`${API_BASE_URL}/v2/portfolio/prices`);
    return response.data;
  },

  // Get main DDD token data
  getDDDToken: async () => {
    const response = await axios.get(`${API_BASE_URL}/v2/portfolio/ddd`);
    return response.data;
  },

  // Get DDD token with historical data
  getDDDTokenHistorical: async (days = 30) => {
    const response = await axios.get(`${API_BASE_URL}/v2/portfolio/ddd/historical?days=${days}`);
    return response.data;
  },

  // Get top pairs by liquidity
  getTopPairsByLiquidity: async (limit = 5) => {
    const response = await axios.get(`${API_BASE_URL}/v2/portfolio/pairs/top-liquidity?limit=${limit}`);
    return response.data;
  },

  // Get top pairs by volume
  getTopPairsByVolume: async (limit = 5) => {
    const response = await axios.get(`${API_BASE_URL}/v2/portfolio/pairs/top-volume?limit=${limit}`);
    return response.data;
  },

  // Portfolio health check
  getPortfolioHealth: async () => {
    const response = await axios.get(`${API_BASE_URL}/v2/portfolio/health`);
    return response.data;
  },

  // ============================================================================
  // V2 UNIFIED TOKEN ENDPOINTS
  // ============================================================================

  // Get token with automatic fallback
  getTokenUnified: async (contractAddress, network = 'polygon') => {
    const response = await axios.get(`${API_BASE_URL}/v2/token/${contractAddress}?network=${network}`);
    return response.data;
  },

  // Get token with historical data
  getTokenHistoricalUnified: async (contractAddress, network = 'polygon', days = 30) => {
    const response = await axios.get(
      `${API_BASE_URL}/v2/token/${contractAddress}/historical?network=${network}&days=${days}`
    );
    return response.data;
  },

  // Get token with technical indicators
  getTokenIndicatorsUnified: async (contractAddress, network = 'polygon', days = 30) => {
    const response = await axios.get(
      `${API_BASE_URL}/v2/token/${contractAddress}/indicators?network=${network}&days=${days}`
    );
    return response.data;
  },

  // ============================================================================
  // LEGACY ENDPOINTS (Still supported)
  // ============================================================================
  // Get current price for a single cryptocurrency
  getCurrentPrice: async (symbol) => {
    const response = await axios.get(`${API_BASE_URL}/crypto/price/${symbol}`);
    return response.data;
  },

  // Get prices for multiple cryptocurrencies
  getMultiplePrices: async (symbols) => {
    const symbolsStr = symbols.join(',');
    const response = await axios.get(`${API_BASE_URL}/crypto/prices?symbols=${symbolsStr}`);
    return response.data;
  },

  // Get historical data
  getHistoricalData: async (symbol, days = 30, interval = 'daily') => {
    const response = await axios.get(
      `${API_BASE_URL}/crypto/historical/${symbol}?days=${days}&interval=${interval}`
    );
    return response.data;
  },

  // Get technical indicators
  getTechnicalIndicators: async (symbol, days = 30, interval = 'daily') => {
    const response = await axios.get(
      `${API_BASE_URL}/crypto/indicators/${symbol}?days=${days}&interval=${interval}`
    );
    return response.data;
  },

  // Get top cryptocurrencies
  getTopCryptocurrencies: async (limit = 20) => {
    const response = await axios.get(`${API_BASE_URL}/crypto/top?limit=${limit}`);
    return response.data;
  },

  // Get token by contract address
  getTokenByContract: async (contractAddress, platform = 'ethereum') => {
    const response = await axios.get(
      `${API_BASE_URL}/crypto/token/contract/${contractAddress}?platform=${platform}`
    );
    return response.data;
  },

  // Get token historical data by coin_id
  getTokenHistoricalData: async (coinId, days = 30) => {
    const response = await axios.get(
      `${API_BASE_URL}/crypto/token/${coinId}/historical?days=${days}`
    );
    return response.data;
  },

  // Get token technical indicators by coin_id
  getTokenIndicators: async (coinId, days = 30) => {
    const response = await axios.get(
      `${API_BASE_URL}/crypto/token/${coinId}/indicators?days=${days}`
    );
    return response.data;
  }
};

export default cryptoAPI;

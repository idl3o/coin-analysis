import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const cryptoAPI = {
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

// Custom ERC-20 tokens to track on the dashboard
export const CUSTOM_TOKENS = [
  {
    symbol: 'DDD',
    name: 'DDD Token',
    contractAddress: '0x4bf82cf0d6b2afc87367052b793097153c859d38',
    platform: 'ethereum',
    isCustomToken: true
  },
  {
    symbol: 'xaIREGEN',
    name: 'xaIREGEN',
    contractAddress: '0xdfffe0c33b4011c4218acd61e68a62a32eaf9a8b',
    platform: 'ethereum',
    isCustomToken: true
  }
];

// Helper function to get token by contract address
export const getTokenByContract = (contractAddress) => {
  return CUSTOM_TOKENS.find(
    token => token.contractAddress.toLowerCase() === contractAddress.toLowerCase()
  );
};

// Helper function to check if symbol is a custom token
export const isCustomToken = (symbol) => {
  return CUSTOM_TOKENS.some(
    token => token.symbol.toUpperCase() === symbol.toUpperCase()
  );
};

export default CUSTOM_TOKENS;

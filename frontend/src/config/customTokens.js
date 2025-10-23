// DDD Token Portfolio Configuration
// All tokens are on Polygon network

export const MAIN_TOKEN = {
  symbol: 'DDD',
  name: 'Durgan Dynasty Doubloon',
  contractAddress: '0x4bf82cf0d6b2afc87367052b793097153c859d38',
  platform: 'polygon',
  isMainToken: true,
  isCustomToken: true
};

export const QUOTE_TOKENS = [
  {
    symbol: 'USDGLO',
    name: 'USDGLO',
    pair: 'DDD/USDGLO',
    contractAddress: '0x7ee2dd0022e3460177b90b8f8fa3b3a76d970ff6',
    platform: 'polygon',
    isCustomToken: true
  },
  {
    symbol: 'axiREGEN',
    name: 'axiREGEN',
    pair: 'DDD/axiREGEN',
    contractAddress: '0x520a3b3faca7ddc8dc8cd3380c8475b67f3c7b8d',
    platform: 'polygon',
    isCustomToken: true
  },
  {
    symbol: 'CCC',
    name: 'CCC',
    pair: 'DDD/CCC',
    contractAddress: '0x73e6a1630486d0874ec56339327993a3e4684691',
    platform: 'polygon',
    isCustomToken: true
  },
  {
    symbol: 'PR24',
    name: 'PR24',
    pair: 'DDD/PR24',
    contractAddress: '0xa249cc5719da5457b212d9c5f4b1e95c7f597441',
    platform: 'polygon',
    isCustomToken: true
  },
  {
    symbol: 'NCT',
    name: 'NCT',
    pair: 'DDD/NCT',
    contractAddress: '0xfc983c854683b562c6e0f858a15b32698b32ba45',
    platform: 'polygon',
    isCustomToken: true
  },
  {
    symbol: 'JCGWR',
    name: 'JCGWR',
    pair: 'DDD/JCGWR',
    contractAddress: '0x7aadf47b49202b904b0f62e533442b09fcaa2614',
    platform: 'polygon',
    isCustomToken: true
  },
  {
    symbol: 'AU24T',
    name: 'AU24T',
    pair: 'DDD/AU24T',
    contractAddress: '0xdaa015423b5965f1b198119cd8940e0e551cd74c',
    platform: 'polygon',
    isCustomToken: true
  },
  {
    symbol: 'JLT-F24',
    name: 'JLT-F24',
    pair: 'DDD/JLT-F24',
    contractAddress: '0x4faf57a632bd809974358a5fff9ae4aec5a51b7d',
    platform: 'polygon',
    isCustomToken: true
  },
  {
    symbol: 'JLT-F24-2',
    name: 'JLT-F24 (v2)',
    pair: 'DDD/JLT-F24',
    contractAddress: '0xf2bda2e42fbd1ec6ee61b9e11aeb690eb88956c1',
    platform: 'polygon',
    isCustomToken: true
  }
];

export const LP_POOLS = [
  {
    pair: 'DDD/JLT-B23',
    poolAddress: '0xac6c98888209c2cccb500e0b1afb70fb2474611b1520d4f55e1968518179f40c',
    platform: 'polygon',
    type: 'pool'
  },
  {
    pair: 'DDD/TB01',
    poolAddress: '0x54c0a64be7d50e9a8e6b7de50055982934b3d09bfaedfff6cc1c5190d0ba83d7',
    platform: 'polygon',
    type: 'pool'
  },
  {
    pair: 'DDD/MC02',
    poolAddress: '0xebb0ef84907875a6004d89268df1534c6a8dff2441e653c90f1c07f51adcfb8a',
    platform: 'polygon',
    type: 'pool'
  }
];

// All tokens (for iteration)
export const ALL_TOKENS = [MAIN_TOKEN, ...QUOTE_TOKENS];

// Legacy export for backwards compatibility
export const CUSTOM_TOKENS = ALL_TOKENS;

// Helper functions
export const getTokenByContract = (contractAddress) => {
  return ALL_TOKENS.find(
    token => token.contractAddress.toLowerCase() === contractAddress.toLowerCase()
  );
};

export const getTokenBySymbol = (symbol) => {
  return ALL_TOKENS.find(
    token => token.symbol.toUpperCase() === symbol.toUpperCase()
  );
};

export const isCustomToken = (symbol) => {
  return ALL_TOKENS.some(
    token => token.symbol.toUpperCase() === symbol.toUpperCase()
  );
};

export const getPoolByPair = (pairName) => {
  return LP_POOLS.find(
    pool => pool.pair.toUpperCase() === pairName.toUpperCase()
  );
};

export default {
  MAIN_TOKEN,
  QUOTE_TOKENS,
  LP_POOLS,
  ALL_TOKENS,
  CUSTOM_TOKENS,
  getTokenByContract,
  getTokenBySymbol,
  isCustomToken,
  getPoolByPair
};

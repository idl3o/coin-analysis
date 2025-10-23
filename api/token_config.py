"""
Token Portfolio Configuration
All tokens are on Polygon network
"""

# Main token to track
MAIN_TOKEN = {
    "symbol": "DDD",
    "name": "DDD Token",
    "contract": "0x4bf82cf0d6b2afc87367052b793097153c859d38",
    "network": "polygon",
    "type": "token"
}

# Quote tokens (tokens paired with DDD)
QUOTE_TOKENS = [
    {
        "symbol": "USDGLO",
        "pair": "DDD/USDGLO",
        "contract": "0x7ee2dd0022e3460177b90b8f8fa3b3a76d970ff6",
        "network": "polygon",
        "type": "token"
    },
    {
        "symbol": "axiREGEN",
        "pair": "DDD/axiREGEN",
        "contract": "0x520a3b3faca7ddc8dc8cd3380c8475b67f3c7b8d",
        "network": "polygon",
        "type": "token"
    },
    {
        "symbol": "CCC",
        "pair": "DDD/CCC",
        "contract": "0x73e6a1630486d0874ec56339327993a3e4684691",
        "network": "polygon",
        "type": "token"
    },
    {
        "symbol": "PR24",
        "pair": "DDD/PR24",
        "contract": "0xa249cc5719da5457b212d9c5f4b1e95c7f597441",
        "network": "polygon",
        "type": "token"
    },
    {
        "symbol": "NCT",
        "pair": "DDD/NCT",
        "contract": "0xfc983c854683b562c6e0f858a15b32698b32ba45",
        "network": "polygon",
        "type": "token"
    },
    {
        "symbol": "JCGWR",
        "pair": "DDD/JCGWR",
        "contract": "0x7aadf47b49202b904b0f62e533442b09fcaa2614",
        "network": "polygon",
        "type": "token"
    },
    {
        "symbol": "AU24T",
        "pair": "DDD/AU24T",
        "contract": "0xdaa015423b5965f1b198119cd8940e0e551cd74c",
        "network": "polygon",
        "type": "token"
    },
    {
        "symbol": "JLT-F24",
        "pair": "DDD/JLT-F24",
        "contract": "0x4faf57a632bd809974358a5fff9ae4aec5a51b7d",
        "network": "polygon",
        "type": "token"
    },
    {
        "symbol": "JLT-F24-2",  # Second JLT-F24 token with different address
        "pair": "DDD/JLT-F24",
        "contract": "0xf2bda2e42fbd1ec6ee61b9e11aeb690eb88956c1",
        "network": "polygon",
        "type": "token"
    }
]

# Liquidity Pool addresses (64-character addresses)
# These are the actual LP pairs, not individual tokens
LP_POOLS = [
    {
        "pair": "DDD/JLT-B23",
        "pool_address": "0xac6c98888209c2cccb500e0b1afb70fb2474611b1520d4f55e1968518179f40c",
        "network": "polygon",
        "type": "pool"
    },
    {
        "pair": "DDD/TB01",
        "pool_address": "0x54c0a64be7d50e9a8e6b7de50055982934b3d09bfaedfff6cc1c5190d0ba83d7",
        "network": "polygon",
        "type": "pool"
    },
    {
        "pair": "DDD/MC02",
        "pool_address": "0xebb0ef84907875a6004d89268df1534c6a8dff2441e653c90f1c07f51adcfb8a",
        "network": "polygon",
        "type": "pool"
    }
]

# All tokens to track (for easy iteration)
ALL_TOKENS = [MAIN_TOKEN] + QUOTE_TOKENS

# Get all unique token addresses
def get_all_token_addresses():
    """Get list of all token addresses"""
    return [token["contract"] for token in ALL_TOKENS]

# Get all pool addresses
def get_all_pool_addresses():
    """Get list of all LP pool addresses"""
    return [pool["pool_address"] for pool in LP_POOLS]

# Get token by address
def get_token_by_address(address: str):
    """Find token config by address"""
    address = address.lower()
    for token in ALL_TOKENS:
        if token["contract"].lower() == address:
            return token
    return None

# Get pool by address
def get_pool_by_address(address: str):
    """Find pool config by address"""
    address = address.lower()
    for pool in LP_POOLS:
        if pool["pool_address"].lower() == address:
            return pool
    return None

# Portfolio summary
PORTFOLIO = {
    "name": "DDD Portfolio",
    "network": "polygon",
    "main_token": MAIN_TOKEN,
    "quote_tokens": QUOTE_TOKENS,
    "lp_pools": LP_POOLS,
    "total_pairs": len(QUOTE_TOKENS) + len(LP_POOLS)
}

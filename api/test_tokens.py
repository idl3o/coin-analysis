"""
Test script to check which APIs work for our tokens
"""
import asyncio
import sys
from token_config import MAIN_TOKEN, QUOTE_TOKENS, LP_POOLS
from unified_price_service import UnifiedPriceService


async def test_token(contract_address: str, symbol: str, network: str = "polygon"):
    """Test a single token against all APIs"""
    print(f"\n{'='*60}")
    print(f"Testing: {symbol}")
    print(f"Address: {contract_address}")
    print(f"Network: {network}")
    print(f"{'='*60}")

    unified = UnifiedPriceService()

    try:
        # Test with unified service (tries all sources)
        result = await unified.compare_sources(contract_address, network)

        print(f"\n[OK] RESULTS FOR {symbol}:")
        print(f"Timestamp: {result['timestamp']}")

        # Check each source
        for source_name, source_data in result['sources'].items():
            if source_data['success']:
                print(f"\n  [SUCCESS] {source_name.upper()}")
                if source_data.get('price'):
                    print(f"    Price: ${source_data['price']}")
                if source_data.get('data'):
                    data = source_data['data']
                    if 'name' in data:
                        print(f"    Name: {data.get('name', 'N/A')}")
                    if 'symbol' in data:
                        print(f"    Symbol: {data.get('symbol', 'N/A')}")
                    if 'volume_24h' in data:
                        print(f"    Volume 24h: ${data.get('volume_24h', 0):,.2f}")
                    if 'liquidity_usd' in data:
                        print(f"    Liquidity: ${data.get('liquidity_usd', 0):,.2f}")
            else:
                print(f"\n  [FAILED] {source_name.upper()}")
                print(f"    Error: {source_data.get('error', 'Unknown error')}")

        # Price analysis
        if 'price_analysis' in result:
            analysis = result['price_analysis']
            print(f"\n  PRICE ANALYSIS:")
            print(f"    Average Price: ${analysis['average']:,.8f}")
            print(f"    Max Deviation: {analysis['max_deviation_percent']:.2f}%")
            print(f"    Consistent: {'YES' if analysis['consistent'] else 'NO'}")

        return result

    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        return None
    finally:
        await unified.close()


async def test_all_tokens():
    """Test all tokens in the portfolio"""
    print("\n" + "="*60)
    print("TESTING DDD PORTFOLIO TOKENS")
    print("="*60)

    results = {
        "main_token": None,
        "quote_tokens": [],
        "summary": {
            "total": 0,
            "geckoterminal_success": 0,
            "defillama_success": 0,
            "alchemy_success": 0,
            "no_price_data": 0
        }
    }

    # Test main token
    print("\n\n### MAIN TOKEN ###")
    main_result = await test_token(
        MAIN_TOKEN["contract"],
        MAIN_TOKEN["symbol"],
        MAIN_TOKEN["network"]
    )
    results["main_token"] = main_result

    # Test quote tokens
    print("\n\n### QUOTE TOKENS ###")
    for token in QUOTE_TOKENS:
        result = await test_token(
            token["contract"],
            token["symbol"],
            token["network"]
        )
        results["quote_tokens"].append({
            "symbol": token["symbol"],
            "result": result
        })

        # Small delay to avoid rate limiting
        await asyncio.sleep(2)

    # Analyze results
    print("\n\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    all_results = [results["main_token"]] + [r["result"] for r in results["quote_tokens"]]

    for result in all_results:
        if result:
            results["summary"]["total"] += 1
            sources = result.get("sources", {})

            if sources.get("geckoterminal", {}).get("success"):
                results["summary"]["geckoterminal_success"] += 1
            if sources.get("defillama", {}).get("success"):
                results["summary"]["defillama_success"] += 1
            if sources.get("alchemy", {}).get("success"):
                results["summary"]["alchemy_success"] += 1

            # Check if any source has price
            has_price = any(
                s.get("price") is not None
                for s in sources.values()
                if s.get("success")
            )
            if not has_price:
                results["summary"]["no_price_data"] += 1

    summary = results["summary"]
    print(f"\nTotal Tokens Tested: {summary['total']}")
    print(f"GeckoTerminal Success: {summary['geckoterminal_success']}/{summary['total']}")
    print(f"DeFiLlama Success: {summary['defillama_success']}/{summary['total']}")
    print(f"Alchemy Success: {summary['alchemy_success']}/{summary['total']}")
    print(f"No Price Data: {summary['no_price_data']}/{summary['total']}")

    # LP Pools note
    if LP_POOLS:
        print(f"\n[NOTE]: {len(LP_POOLS)} LP Pool addresses detected.")
        print("   Pool addresses require special handling (use pool endpoints).")
        print("   Pools:", [p["pair"] for p in LP_POOLS])

    return results


async def test_single_token_quick():
    """Quick test of just the DDD token"""
    print("Quick test: DDD Token only")
    result = await test_token(
        MAIN_TOKEN["contract"],
        MAIN_TOKEN["symbol"],
        MAIN_TOKEN["network"]
    )
    return result


if __name__ == "__main__":
    # Check command line args
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        asyncio.run(test_single_token_quick())
    else:
        asyncio.run(test_all_tokens())

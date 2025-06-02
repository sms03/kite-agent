"""
Example script demonstrating Zerodha AI Agent capabilities
"""

import asyncio
import json
from datetime import datetime, timedelta
from app.agent import zerodha_agent

async def demo_portfolio_analysis():
    """Demonstrate portfolio analysis capabilities"""
    print("🔍 DEMO: Portfolio Analysis")
    print("="*40)
    
    # Get portfolio summary
    portfolio = await zerodha_agent.get_portfolio_summary()
    
    if 'error' not in portfolio:
        summary = portfolio.get('summary', {})
        print(f"📊 Portfolio Value: ₹{summary.get('current_value', 0):,.2f}")
        print(f"📈 Total P&L: ₹{summary.get('total_pnl', 0):,.2f}")
        print(f"📊 Return: {summary.get('return_percentage', 0):.2f}%")
        print(f"💳 Available Cash: ₹{summary.get('available_margin', 0):,.2f}")
        
        holdings_count = len(portfolio.get('holdings', {}).get('data', []))
        positions_count = len(portfolio.get('positions', {}).get('data', []))
        print(f"📦 Holdings: {holdings_count} stocks")
        print(f"📍 Active Positions: {positions_count}")
    else:
        print(f"❌ Error: {portfolio['error']}")

async def demo_market_data():
    """Demonstrate market data fetching"""
    print("\n💹 DEMO: Live Market Data")
    print("="*40)
    
    # Popular stocks for demo
    popular_stocks = ["NSE:INFY", "NSE:TCS", "NSE:RELIANCE", "NSE:HDFCBANK"]
    
    quotes = await zerodha_agent.get_live_quotes(popular_stocks)
    
    if quotes:
        for symbol, data in quotes.items():
            if isinstance(data, dict):
                price = data.get('last_price', 0)
                change = data.get('net_change', 0)
                change_pct = data.get('change_percent', 0)
                volume = data.get('volume', 0)
                
                direction = "📈" if change >= 0 else "📉"
                print(f"{direction} {symbol}: ₹{price:.2f} ({change:+.2f}, {change_pct:+.2f}%) Vol: {volume:,}")
    else:
        print("❌ No market data available")

async def demo_instrument_search():
    """Demonstrate instrument search"""
    print("\n🔍 DEMO: Instrument Search")
    print("="*40)
    
    # Search for IT companies
    search_terms = ["INFY", "TCS", "WIPRO"]
    
    for term in search_terms:
        instruments = await zerodha_agent.search_instruments(term)
        if instruments:
            instrument = instruments[0]  # Take first result
            print(f"🔍 {term}: {instrument.get('name', 'N/A')} ({instrument.get('exchange', 'N/A')})")

async def demo_market_analysis():
    """Demonstrate AI-powered market analysis"""
    print("\n🤖 DEMO: AI Market Analysis")
    print("="*40)
    
    # Analyze some popular stocks
    stocks_to_analyze = ["NSE:INFY", "NSE:TCS", "NSE:WIPRO"]
    
    analysis = await zerodha_agent.analyze_market_data(stocks_to_analyze)
    
    if analysis:
        for symbol, data in analysis.items():
            price = data.get('current_price', 0)
            change_pct = data.get('change_percent', 0)
            recommendation = data.get('recommendation', 'No recommendation')
            
            trend_emoji = "🚀" if change_pct > 2 else "📈" if change_pct > 0 else "📉" if change_pct < -2 else "➡️"
            print(f"{trend_emoji} {symbol.split(':')[1]}: ₹{price:.2f} ({change_pct:+.2f}%)")
            print(f"   💡 AI Recommendation: {recommendation}")

async def demo_order_simulation():
    """Demonstrate order placement (simulation mode)"""
    print("\n📊 DEMO: Order Placement Simulation")
    print("="*40)
    print("ℹ️  This is a simulation - no real orders will be placed")
    
    # Simulate order parameters
    order_params = {
        'exchange': 'NSE',
        'trading_symbol': 'INFY',
        'transaction_type': 'BUY',
        'quantity': 1,
        'order_type': 'LIMIT',
        'product': 'CNC',
        'price': 1500.0
    }
    
    print(f"📋 Simulated Order:")
    print(f"   📈 {order_params['transaction_type']} {order_params['quantity']} shares")
    print(f"   🏢 Stock: {order_params['trading_symbol']} ({order_params['exchange']})")
    print(f"   💰 Price: ₹{order_params['price']}")
    print(f"   📦 Product: {order_params['product']}")
    print(f"   🎯 Type: {order_params['order_type']}")
    
    print("\n⚠️  To place real orders, use the interactive menu or call:")
    print("   await zerodha_agent.place_order(**order_params)")

async def demo_historical_data():
    """Demonstrate historical data fetching"""
    print("\n📈 DEMO: Historical Data")
    print("="*40)
    print("ℹ️  Historical data requires instrument tokens from search")
    
    # Example: Show how to get historical data
    print("📊 To get historical data:")
    print("1. Search for instrument: await zerodha_agent.search_instruments('INFY')")
    print("2. Get instrument token from search results")
    print("3. Call: await zerodha_agent.get_historical_data(token, from_date, to_date)")
    
    # Show date format
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    print(f"\n📅 Example date format:")
    print(f"   From: {week_ago.strftime('%Y-%m-%d')}")
    print(f"   To: {today.strftime('%Y-%m-%d')}")

async def run_comprehensive_demo():
    """Run comprehensive demo of all features"""
    print("🚀 ZERODHA AI AGENT - COMPREHENSIVE DEMO")
    print("="*50)
    
    try:
        # Initialize agent
        print("🔧 Initializing Zerodha AI Agent...")
        success = await zerodha_agent.initialize()
        
        if not success:
            print("❌ Failed to initialize. Running in demo mode...")
            print("ℹ️  Some features require valid Zerodha credentials")
        else:
            print("✅ Agent initialized successfully!")
        
        # Run all demos
        await demo_portfolio_analysis()
        await demo_market_data()
        await demo_instrument_search()
        await demo_market_analysis()
        await demo_order_simulation()
        await demo_historical_data()
        
        print("\n" + "="*50)
        print("🎉 DEMO COMPLETED")
        print("="*50)
        print("✨ The Zerodha AI Agent provides:")
        print("   📊 Portfolio management and analysis")
        print("   💹 Real-time market data")
        print("   🤖 AI-powered trading recommendations")
        print("   📈 Order placement and management")
        print("   📊 Historical data analysis")
        print("   ⏰ Advanced order types (GTT, etc.)")
        
        print("\n🚀 Ready to start trading with AI assistance!")
        print("   Run 'python main.py' for interactive mode")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("ℹ️  This might be due to missing Zerodha credentials")

if __name__ == "__main__":
    try:
        asyncio.run(run_comprehensive_demo())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

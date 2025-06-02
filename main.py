"""
Main entry point for the Zerodha AI Agent
"""

import asyncio
import json
from app.agent import zerodha_agent

async def main():
    """Main function to demonstrate the Zerodha AI Agent capabilities"""
    
    print("🚀 Initializing Zerodha AI Agent...")
    
    # Initialize the agent
    success = await zerodha_agent.initialize()
    if not success:
        print("❌ Failed to initialize agent. Please check your Zerodha credentials.")
        return
    
    print("✅ Agent initialized successfully!")
    
    # Menu-driven interface
    while True:
        print("\n" + "="*50)
        print("📊 ZERODHA AI AGENT - TRADING ASSISTANT")
        print("="*50)
        print("1. 📈 Get Portfolio Summary")
        print("2. 🔍 Search Instruments")
        print("3. 💹 Get Live Market Data")
        print("4. 📊 Place Order")
        print("5. 📋 View Orders")
        print("6. 📈 Get Historical Data")
        print("7. ⏰ GTT Orders")
        print("8. 🔄 Market Analysis")
        print("9. ❌ Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-9): ").strip()
        
        try:
            if choice == "1":
                await handle_portfolio_summary()
            elif choice == "2":
                await handle_search_instruments()
            elif choice == "3":
                await handle_live_market_data()
            elif choice == "4":
                await handle_place_order()
            elif choice == "5":
                await handle_view_orders()
            elif choice == "6":
                await handle_historical_data()
            elif choice == "7":
                await handle_gtt_orders()
            elif choice == "8":
                await handle_market_analysis()
            elif choice == "9":
                print("👋 Thank you for using Zerodha AI Agent!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except Exception as e:
            print(f"❌ Error: {e}")

async def handle_portfolio_summary():
    """Handle portfolio summary display"""
    print("\n📊 Fetching Portfolio Summary...")
    portfolio = await zerodha_agent.get_portfolio_summary()
    
    if 'error' in portfolio:
        print(f"❌ Error: {portfolio['error']}")
        return
    
    print("\n" + "="*40)
    print("📈 PORTFOLIO SUMMARY")
    print("="*40)
    
    if 'summary' in portfolio:
        summary = portfolio['summary']
        print(f"💰 Total Invested: ₹{summary.get('total_invested', 0):,.2f}")
        print(f"💵 Current Value: ₹{summary.get('current_value', 0):,.2f}")
        print(f"📈 Total P&L: ₹{summary.get('total_pnl', 0):,.2f}")
        print(f"📊 Return %: {summary.get('return_percentage', 0):.2f}%")
        print(f"💳 Available Margin: ₹{summary.get('available_margin', 0):,.2f}")
    
    print(f"\n📦 Holdings: {len(portfolio.get('holdings', {}).get('data', []))} stocks")
    print(f"📍 Positions: {len(portfolio.get('positions', {}).get('data', []))} active")

async def handle_search_instruments():
    """Handle instrument search"""
    query = input("\n🔍 Enter instrument name to search: ").strip()
    if not query:
        print("❌ Please enter a valid search term.")
        return
    
    print(f"🔍 Searching for '{query}'...")
    instruments = await zerodha_agent.search_instruments(query)
    
    if not instruments:
        print("❌ No instruments found.")
        return
    
    print(f"\n📋 Found {len(instruments)} instruments:")
    for i, instrument in enumerate(instruments[:10], 1):  # Show top 10
        print(f"{i}. {instrument.get('tradingsymbol', 'N/A')} - {instrument.get('name', 'N/A')} ({instrument.get('exchange', 'N/A')})")

async def handle_live_market_data():
    """Handle live market data display"""
    symbols = input("\n💹 Enter instrument symbols (comma-separated, e.g., NSE:INFY,NSE:TCS): ").strip()
    if not symbols:
        print("❌ Please enter valid symbols.")
        return
    
    instruments = [s.strip() for s in symbols.split(',')]
    print(f"📊 Fetching live data for {instruments}...")
    
    quotes = await zerodha_agent.get_live_quotes(instruments)
    
    if not quotes:
        print("❌ No data found.")
        return
    
    print("\n" + "="*60)
    print("💹 LIVE MARKET DATA")
    print("="*60)
    
    for symbol, data in quotes.items():
        if isinstance(data, dict):
            print(f"\n📈 {symbol}:")
            print(f"  💰 Price: ₹{data.get('last_price', 0)}")
            print(f"  📊 Change: ₹{data.get('net_change', 0)} ({data.get('change_percent', 0):.2f}%)")
            print(f"  📈 High: ₹{data.get('ohlc', {}).get('high', 0)}")
            print(f"  📉 Low: ₹{data.get('ohlc', {}).get('low', 0)}")
            print(f"  📦 Volume: {data.get('volume', 0):,}")

async def handle_place_order():
    """Handle order placement"""
    print("\n📊 PLACE ORDER")
    print("="*30)
    
    # Get order details
    exchange = input("Exchange (NSE/BSE/NFO/BFO/MCX): ").strip().upper()
    if exchange not in ["NSE", "BSE", "NFO", "BFO", "MCX"]:
        print("❌ Invalid exchange.")
        return
    
    symbol = input("Trading Symbol (e.g., INFY, TCS): ").strip().upper()
    transaction_type = input("Transaction Type (BUY/SELL): ").strip().upper()
    
    if transaction_type not in ["BUY", "SELL"]:
        print("❌ Invalid transaction type.")
        return
    
    try:
        quantity = int(input("Quantity: ").strip())
        if quantity <= 0:
            print("❌ Quantity must be positive.")
            return
    except ValueError:
        print("❌ Invalid quantity.")
        return
    
    order_type = input("Order Type (MARKET/LIMIT/SL/SL-M): ").strip().upper()
    if order_type not in ["MARKET", "LIMIT", "SL", "SL-M"]:
        print("❌ Invalid order type.")
        return
    
    product = input("Product (CNC/MIS/NRML): ").strip().upper()
    if product not in ["CNC", "MIS", "NRML"]:
        print("❌ Invalid product type.")
        return
    
    price = None
    trigger_price = None
    
    if order_type in ["LIMIT", "SL"]:
        try:
            price = float(input("Limit Price: ").strip())
        except ValueError:
            print("❌ Invalid price.")
            return
    
    if order_type in ["SL", "SL-M"]:
        try:
            trigger_price = float(input("Trigger Price: ").strip())
        except ValueError:
            print("❌ Invalid trigger price.")
            return
    
    # Confirmation
    print(f"\n📋 Order Summary:")
    print(f"  📈 {transaction_type} {quantity} shares of {symbol}")
    print(f"  📊 Exchange: {exchange}")
    print(f"  📦 Product: {product}")
    print(f"  🎯 Order Type: {order_type}")
    if price:
        print(f"  💰 Price: ₹{price}")
    if trigger_price:
        print(f"  ⚡ Trigger Price: ₹{trigger_price}")
    
    confirm = input("\n⚠️  Confirm order placement? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❌ Order cancelled.")
        return
    
    print("📤 Placing order...")
    result = await zerodha_agent.place_order(
        exchange=exchange,
        trading_symbol=symbol,
        transaction_type=transaction_type,
        quantity=quantity,
        order_type=order_type,
        product=product,
        price=price,
        trigger_price=trigger_price
    )
    
    if 'error' in result:
        print(f"❌ Order failed: {result['error']}")
    else:
        print("✅ Order placed successfully!")
        if 'data' in result and 'order_id' in result['data']:
            print(f"📋 Order ID: {result['data']['order_id']}")

async def handle_view_orders():
    """Handle viewing orders"""
    print("\n📋 Fetching Orders...")
    orders = await zerodha_agent.get_orders()
    
    if not orders:
        print("❌ No orders found.")
        return
    
    print("\n" + "="*80)
    print("📋 ORDERS")
    print("="*80)
    
    for order in orders:
        status_emoji = "✅" if order.get('status') == 'COMPLETE' else "⏳" if order.get('status') == 'OPEN' else "❌"
        print(f"{status_emoji} {order.get('tradingsymbol', 'N/A')} | {order.get('transaction_type', 'N/A')} | "
              f"Qty: {order.get('quantity', 0)} | Price: ₹{order.get('price', 0)} | "
              f"Status: {order.get('status', 'N/A')}")

async def handle_historical_data():
    """Handle historical data fetching"""
    print("\n📈 Historical Data")
    print("Note: You need instrument token for this. Use search instruments first.")
    
    try:
        token = int(input("Instrument Token: ").strip())
        from_date = input("From Date (YYYY-MM-DD): ").strip()
        to_date = input("To Date (YYYY-MM-DD): ").strip()
        interval = input("Interval (minute/day/5minute/15minute/30minute/60minute) [day]: ").strip() or "day"
        
        print("📊 Fetching historical data...")
        data = await zerodha_agent.get_historical_data(token, from_date, to_date, interval)
        
        if not data:
            print("❌ No data found.")
            return
        
        print(f"\n📈 Historical Data ({len(data)} records):")
        print("Date\t\tOpen\tHigh\tLow\tClose\tVolume")
        print("-" * 60)
        
        for record in data[-10:]:  # Show last 10 records
            print(f"{record.get('date', 'N/A')}\t₹{record.get('open', 0):.2f}\t₹{record.get('high', 0):.2f}\t"
                  f"₹{record.get('low', 0):.2f}\t₹{record.get('close', 0):.2f}\t{record.get('volume', 0):,}")
    
    except ValueError:
        print("❌ Invalid input.")

async def handle_gtt_orders():
    """Handle GTT orders"""
    print("\n⏰ GTT Orders")
    print("1. View GTT Orders")
    print("2. Place GTT Order")
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        print("📋 Fetching GTT orders...")
        gtt_orders = await zerodha_agent.get_gtt_orders()
        
        if not gtt_orders:
            print("❌ No GTT orders found.")
            return
        
        print(f"\n⏰ Found {len(gtt_orders)} GTT orders:")
        for gtt in gtt_orders:
            print(f"ID: {gtt.get('id', 'N/A')} | {gtt.get('tradingsymbol', 'N/A')} | "
                  f"Type: {gtt.get('trigger_type', 'N/A')} | Status: {gtt.get('status', 'N/A')}")
    
    elif choice == "2":
        print("📊 GTT Order placement is complex. Please use the API documentation for detailed implementation.")

async def handle_market_analysis():
    """Handle market analysis"""
    symbols = input("\n🔄 Enter symbols for analysis (comma-separated): ").strip()
    if not symbols:
        print("❌ Please enter valid symbols.")
        return
    
    instruments = [s.strip() for s in symbols.split(',')]
    print("🔍 Analyzing market data...")
    
    analysis = await zerodha_agent.analyze_market_data(instruments)
    
    if not analysis:
        print("❌ No analysis data available.")
        return
    
    print("\n" + "="*70)
    print("🔄 MARKET ANALYSIS")
    print("="*70)
    
    for symbol, data in analysis.items():
        print(f"\n📈 {symbol}:")
        print(f"  💰 Current Price: ₹{data.get('current_price', 0)}")
        print(f"  📊 Change: ₹{data.get('change', 0)} ({data.get('change_percent', 0):.2f}%)")
        print(f"  📦 Volume: {data.get('volume', 0):,}")
        print(f"  💡 Recommendation: {data.get('recommendation', 'N/A')}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

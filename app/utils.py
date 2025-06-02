"""
Utility functions for the Zerodha AI Agent
"""

import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class TradingUtils:
    """Utility functions for trading operations"""
    
    @staticmethod
    def format_currency(amount: Union[int, float]) -> str:
        """Format amount as Indian currency"""
        return f"₹{amount:,.2f}"
    
    @staticmethod
    def format_percentage(percentage: Union[int, float]) -> str:
        """Format percentage with proper sign"""
        sign = "+" if percentage >= 0 else ""
        return f"{sign}{percentage:.2f}%"
    
    @staticmethod
    def calculate_pnl_percentage(invested: float, current: float) -> float:
        """Calculate P&L percentage"""
        if invested == 0:
            return 0.0
        return ((current - invested) / invested) * 100
    
    @staticmethod
    def validate_trading_symbol(symbol: str) -> bool:
        """Validate trading symbol format"""
        # Basic validation for Indian stock symbols
        pattern = r'^[A-Z0-9&-]+$'
        return bool(re.match(pattern, symbol.upper()))
    
    @staticmethod
    def parse_instrument_identifier(identifier: str) -> Dict[str, str]:
        """Parse instrument identifier like 'NSE:INFY' into exchange and symbol"""
        if ':' in identifier:
            exchange, symbol = identifier.split(':', 1)
            return {'exchange': exchange.upper(), 'symbol': symbol.upper()}
        else:
            return {'exchange': 'NSE', 'symbol': identifier.upper()}
    
    @staticmethod
    def format_instrument_identifier(exchange: str, symbol: str) -> str:
        """Format exchange and symbol into identifier"""
        return f"{exchange.upper()}:{symbol.upper()}"
    
    @staticmethod
    def calculate_order_value(quantity: int, price: float) -> float:
        """Calculate total order value"""
        return quantity * price
    
    @staticmethod
    def calculate_brokerage(order_value: float, order_type: str = "equity") -> float:
        """Calculate approximate brokerage (basic calculation)"""
        if order_type.lower() == "equity":
            # Zerodha equity brokerage: ₹20 or 0.03% whichever is lower
            return min(20.0, order_value * 0.0003)
        else:
            # For F&O: ₹20 per executed order
            return 20.0
    
    @staticmethod
    def is_market_open() -> bool:
        """Check if market is currently open (basic check)"""
        now = datetime.now()
        current_time = now.time()
        
        # Market hours: 9:15 AM to 3:30 PM IST
        market_open = datetime.strptime("09:15", "%H:%M").time()
        market_close = datetime.strptime("15:30", "%H:%M").time()
        
        # Check if it's a weekday
        if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False
        
        return market_open <= current_time <= market_close
    
    @staticmethod
    def get_market_status() -> str:
        """Get current market status"""
        if TradingUtils.is_market_open():
            return "🟢 Market Open"
        else:
            now = datetime.now()
            if now.weekday() >= 5:
                return "🔴 Market Closed (Weekend)"
            else:
                current_time = now.time()
                market_open = datetime.strptime("09:15", "%H:%M").time()
                market_close = datetime.strptime("15:30", "%H:%M").time()
                
                if current_time < market_open:
                    return "🟡 Pre-Market"
                else:
                    return "🔴 Post-Market"

class DataFormatter:
    """Utility functions for data formatting and display"""
    
    @staticmethod
    def format_portfolio_summary(portfolio_data: Dict[str, Any]) -> str:
        """Format portfolio summary for display"""
        if 'summary' not in portfolio_data:
            return "❌ No portfolio data available"
        
        summary = portfolio_data['summary']
        lines = [
            "📊 PORTFOLIO SUMMARY",
            "=" * 30,
            f"💰 Total Invested: {TradingUtils.format_currency(summary.get('total_invested', 0))}",
            f"💵 Current Value: {TradingUtils.format_currency(summary.get('current_value', 0))}",
            f"📈 Total P&L: {TradingUtils.format_currency(summary.get('total_pnl', 0))}",
            f"📊 Return: {TradingUtils.format_percentage(summary.get('return_percentage', 0))}",
            f"💳 Available Margin: {TradingUtils.format_currency(summary.get('available_margin', 0))}"
        ]
        
        return "\n".join(lines)
    
    @staticmethod
    def format_holdings_table(holdings: List[Dict[str, Any]]) -> str:
        """Format holdings data as a table"""
        if not holdings:
            return "❌ No holdings data available"
        
        lines = [
            "📦 HOLDINGS",
            "=" * 80,
            f"{'Symbol':<15} {'Qty':<8} {'Avg Price':<12} {'LTP':<12} {'P&L':<12} {'Return %':<10}"
        ]
        lines.append("-" * 80)
        
        for holding in holdings[:10]:  # Show top 10
            symbol = holding.get('tradingsymbol', 'N/A')[:14]
            qty = holding.get('quantity', 0)
            avg_price = holding.get('average_price', 0)
            ltp = holding.get('last_price', 0)
            pnl = holding.get('pnl', 0)
            
            if avg_price > 0:
                return_pct = ((ltp - avg_price) / avg_price) * 100
            else:
                return_pct = 0
            
            pnl_color = "📈" if pnl >= 0 else "📉"
            
            lines.append(
                f"{symbol:<15} {qty:<8} ₹{avg_price:<10.2f} ₹{ltp:<10.2f} "
                f"{pnl_color}₹{pnl:<9.2f} {return_pct:+.2f}%"
            )
        
        return "\n".join(lines)
    
    @staticmethod
    def format_market_quotes(quotes: Dict[str, Any]) -> str:
        """Format market quotes for display"""
        if not quotes:
            return "❌ No market data available"
        
        lines = [
            "💹 LIVE MARKET DATA",
            "=" * 70,
            f"{'Symbol':<15} {'Price':<12} {'Change':<15} {'Volume':<15} {'High/Low':<15}"
        ]
        lines.append("-" * 70)
        
        for symbol, data in quotes.items():
            if isinstance(data, dict):
                price = data.get('last_price', 0)
                change = data.get('net_change', 0)
                change_pct = data.get('change_percent', 0)
                volume = data.get('volume', 0)
                high = data.get('ohlc', {}).get('high', 0)
                low = data.get('ohlc', {}).get('low', 0)
                
                change_color = "📈" if change >= 0 else "📉"
                symbol_short = symbol.split(':')[-1][:14]
                
                lines.append(
                    f"{symbol_short:<15} ₹{price:<10.2f} {change_color}{change:+.2f}({change_pct:+.2f}%) "
                    f"{volume:<15,} {high:.2f}/{low:.2f}"
                )
        
        return "\n".join(lines)
    
    @staticmethod
    def format_orders_table(orders: List[Dict[str, Any]]) -> str:
        """Format orders data as a table"""
        if not orders:
            return "❌ No orders found"
        
        lines = [
            "📋 ORDERS",
            "=" * 90,
            f"{'Symbol':<12} {'Type':<6} {'Qty':<6} {'Price':<10} {'Status':<12} {'Time':<15} {'Order ID':<15}"
        ]
        lines.append("-" * 90)
        
        for order in orders[-20:]:  # Show last 20 orders
            symbol = order.get('tradingsymbol', 'N/A')[:11]
            trans_type = order.get('transaction_type', 'N/A')[:5]
            qty = order.get('quantity', 0)
            price = order.get('price', 0)
            status = order.get('status', 'N/A')[:11]
            order_time = order.get('order_timestamp', 'N/A')[:14]
            order_id = order.get('order_id', 'N/A')[:14]
            
            status_emoji = "✅" if status == 'COMPLETE' else "⏳" if status == 'OPEN' else "❌"
            
            lines.append(
                f"{symbol:<12} {trans_type:<6} {qty:<6} ₹{price:<8.2f} "
                f"{status_emoji}{status:<11} {order_time:<15} {order_id:<15}"
            )
        
        return "\n".join(lines)

class RiskManager:
    """Risk management utilities"""
    
    @staticmethod
    def validate_order_amount(order_value: float, max_amount: float = 100000) -> bool:
        """Validate if order amount is within limits"""
        return order_value <= max_amount
    
    @staticmethod
    def calculate_position_size(portfolio_value: float, risk_percentage: float = 2.0) -> float:
        """Calculate maximum position size based on risk percentage"""
        return portfolio_value * (risk_percentage / 100)
    
    @staticmethod
    def calculate_stop_loss(entry_price: float, stop_loss_pct: float = 5.0, transaction_type: str = "BUY") -> float:
        """Calculate stop loss price"""
        if transaction_type.upper() == "BUY":
            return entry_price * (1 - stop_loss_pct / 100)
        else:  # SELL
            return entry_price * (1 + stop_loss_pct / 100)
    
    @staticmethod
    def get_risk_assessment(change_percent: float, volume: int) -> str:
        """Get risk assessment based on price movement and volume"""
        if abs(change_percent) > 10:
            return "🔴 High Risk - Extreme volatility"
        elif abs(change_percent) > 5:
            return "🟡 Medium Risk - High volatility"
        elif volume < 10000:
            return "🟡 Medium Risk - Low liquidity"
        else:
            return "🟢 Low Risk - Normal conditions"

class Logger:
    """Enhanced logging utilities"""
    
    @staticmethod
    def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
        """Setup logger with proper formatting"""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    @staticmethod
    def log_trade_action(action: str, details: Dict[str, Any]):
        """Log trading actions with details"""
        logger.info(f"TRADE ACTION: {action} - {json.dumps(details, indent=2)}")
    
    @staticmethod
    def log_api_call(endpoint: str, success: bool, response_time: float = None):
        """Log API call results"""
        status = "SUCCESS" if success else "FAILED"
        time_info = f" (took {response_time:.2f}s)" if response_time else ""
        logger.info(f"API CALL: {endpoint} - {status}{time_info}")

# Helper functions for common operations
def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float"""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to int"""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def format_large_number(num: Union[int, float]) -> str:
    """Format large numbers with appropriate suffixes"""
    if num >= 10000000:  # 1 crore
        return f"{num/10000000:.2f}Cr"
    elif num >= 100000:  # 1 lakh
        return f"{num/100000:.2f}L"
    elif num >= 1000:  # 1 thousand
        return f"{num/1000:.1f}K"
    else:
        return f"{num:,.0f}"

def get_trading_session_info() -> Dict[str, Any]:
    """Get current trading session information"""
    now = datetime.now()
    market_status = TradingUtils.get_market_status()
    
    return {
        'current_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'market_status': market_status,
        'is_trading_day': now.weekday() < 5,
        'session_time': 'market' if TradingUtils.is_market_open() else 'closed'
    }

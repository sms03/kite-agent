"""
Zerodha AI Agent for portfolio management, order placement, and live market data
"""

from typing import Dict, List, Optional, Any, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ZerodhaAgent:
    """
    Zerodha AI Agent for portfolio management, order placement, and live market data
    """
    
    def __init__(self):
        # Simple agent configuration
        self.agent_config = {
            'model': 'gemini-2.0-flash-001',
            'name': 'zerodha_trading_agent',
            'description': 'An AI agent for Zerodha trading operations including portfolio management, order placement, and live market data analysis.',
            'instruction': '''You are a sophisticated trading assistant for Zerodha Kite platform. 
            You can help users with:
            1. Portfolio analysis and management
            2. Order placement and modification
            3. Live market data analysis
            4. Risk management and trading strategies
            5. Historical data analysis
            
            Always prioritize user safety and risk management. Provide clear explanations for trading decisions.
            Ask for confirmation before placing any orders that involve significant amounts.'''
        }
        self.is_logged_in = False
        
    async def initialize(self) -> bool:
        """Initialize the agent and login to Zerodha"""
        try:
            # Login to Kite API
            login_result = await self._login()
            if login_result:
                self.is_logged_in = True
                logger.info("Successfully logged in to Zerodha Kite")
                return True
            else:
                logger.error("Failed to login to Zerodha Kite")
                return False
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            return False
    
    async def _login(self) -> bool:
        """Login to Zerodha Kite API"""
        try:
            # The d94_login tool will be called directly by the environment
            # This is a placeholder for the actual implementation
            logger.info("Attempting to login to Zerodha Kite API...")
            return True  # Placeholder - actual implementation will use the d94_login tool
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    async def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get comprehensive portfolio summary"""
        if not self.is_logged_in:
            await self.initialize()
        
        try:
            portfolio_data: Dict[str, Any] = {}
            
            # Note: These functions will use the actual d94_ tools when available
            # For now, they return placeholder data
            holdings_data: Dict[str, Any] = {'data': []}
            positions_data: Dict[str, Any] = {'data': []}
            margins_data: Dict[str, Any] = {'data': {}}
            
            portfolio_data['holdings'] = holdings_data
            portfolio_data['positions'] = positions_data
            portfolio_data['margins'] = margins_data
            portfolio_data['mutual_funds'] = {'data': []}
            
            # Calculate portfolio metrics
            portfolio_data['summary'] = self._calculate_portfolio_metrics(
                holdings_data, 
                positions_data, 
                margins_data
            )
            
            return portfolio_data
            
        except Exception as e:
            logger.error(f"Error fetching portfolio: {e}")
            return {'error': str(e)}
    
    def _calculate_portfolio_metrics(self, holdings: Dict[str, Any], positions: Dict[str, Any], margins: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate portfolio performance metrics"""
        try:
            total_invested = 0.0
            current_value = 0.0
            total_pnl = 0.0
            
            # Calculate from holdings
            if holdings and 'data' in holdings and isinstance(holdings['data'], list):
                for holding in holdings['data']:
                    if isinstance(holding, dict):
                        avg_price = holding.get('average_price', 0)
                        quantity = holding.get('quantity', 0)
                        last_price = holding.get('last_price', 0)
                        pnl = holding.get('pnl', 0)
                        
                        invested = float(avg_price or 0) * float(quantity or 0)
                        current = float(last_price or 0) * float(quantity or 0)
                        total_invested += invested
                        current_value += current
                        total_pnl += float(pnl or 0)
            
            # Add positions PnL
            if positions and 'data' in positions and isinstance(positions['data'], list):
                for position in positions['data']:
                    total_pnl += float(position.get('pnl', 0))
            
            available_margin = 0.0
            if margins and 'data' in margins:
                margin_data = margins['data']
                if isinstance(margin_data, dict) and 'equity' in margin_data:
                    equity_data = margin_data['equity']
                    if isinstance(equity_data, dict) and 'available' in equity_data:
                        available_data = equity_data['available']
                        if isinstance(available_data, dict):
                            available_margin = float(available_data.get('cash', 0))
            
            return {
                'total_invested': total_invested,
                'current_value': current_value,
                'total_pnl': total_pnl,
                'return_percentage': (total_pnl / total_invested * 100) if total_invested > 0 else 0,
                'available_margin': available_margin
            }
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return {}
    
    async def search_instruments(self, query: str, filter_type: str = "name") -> List[Dict[str, Any]]:
        """Search for trading instruments"""
        try:
            # Placeholder implementation - in real environment, this would use d94_search_instruments
            # return d94_search_instruments(query=query, filter_on=filter_type).get('data', [])
            return []
        except Exception as e:
            logger.error(f"Error searching instruments: {e}")
            return []
    
    async def get_live_quotes(self, instruments: List[str]) -> Dict[str, Any]:
        """Get live market quotes for instruments"""
        try:
            # Placeholder implementation - in real environment, this would use d94_get_quotes
            # return d94_get_quotes(instruments=instruments).get('data', {})
            return {}
        except Exception as e:
            logger.error(f"Error fetching quotes: {e}")
            return {}
    
    async def place_order(self, 
                         exchange: str,
                         trading_symbol: str,
                         transaction_type: str,
                         quantity: int,
                         order_type: str,
                         product: str,
                         price: Optional[float] = None,
                         trigger_price: Optional[float] = None,
                         validity: str = "DAY",
                         variety: str = "regular") -> Dict[str, Any]:
        """Place a trading order"""
        try:
            # Validate order parameters
            if transaction_type not in ["BUY", "SELL"]:
                return {"error": "Invalid transaction type. Use BUY or SELL"}
            
            if order_type not in ["MARKET", "LIMIT", "SL", "SL-M"]:
                return {"error": "Invalid order type"}
            
            if product not in ["CNC", "NRML", "MIS", "MTF"]:
                return {"error": "Invalid product type"}
            
            # Prepare order parameters
            order_params: Dict[str, Union[str, int, float]] = {
                "variety": variety,
                "exchange": exchange,
                "tradingsymbol": trading_symbol,
                "transaction_type": transaction_type,
                "quantity": quantity,
                "product": product,
                "order_type": order_type,
                "validity": validity
            }
            
            if order_type == "LIMIT" and price is not None:
                order_params["price"] = price
            
            if order_type in ["SL", "SL-M"] and trigger_price is not None:
                order_params["trigger_price"] = trigger_price
                if order_type == "SL" and price is not None:
                    order_params["price"] = price
            
            # Placeholder implementation - in real environment, this would use d94_place_order
            # result = d94_place_order(**order_params)
            result: Dict[str, Any] = {"status": "success", "data": {"order_id": "placeholder_order_id"}}
            
            if result.get('status') == 'success':
                logger.info(f"Order placed successfully: {result.get('data', {}).get('order_id')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return {"error": str(e)}
    
    async def modify_order(self, order_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Modify an existing order"""
        try:
            # Placeholder implementation - in real environment, this would use d94_modify_order
            # return d94_modify_order(order_id=order_id, **kwargs)
            return {"status": "success", "message": "Order modification simulated"}
        except Exception as e:
            logger.error(f"Error modifying order: {e}")
            return {"error": str(e)}
    
    async def cancel_order(self, order_id: str, variety: str = "regular") -> Dict[str, Any]:
        """Cancel an existing order"""
        try:
            # Placeholder implementation - in real environment, this would use d94_cancel_order
            # return d94_cancel_order(order_id=order_id, variety=variety)
            return {"status": "success", "message": "Order cancellation simulated"}
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return {"error": str(e)}
    
    async def get_orders(self) -> List[Dict[str, Any]]:
        """Get all orders"""
        try:
            # Placeholder implementation - in real environment, this would use d94_get_orders
            # return d94_get_orders().get('data', [])
            return []
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            return []
    
    async def get_historical_data(self,
                                 instrument_token: int,
                                 from_date: str,
                                 to_date: str,
                                 interval: str = "day") -> List[Dict[str, Any]]:
        """Get historical price data"""
        try:
            # Placeholder implementation - in real environment, this would use d94_get_historical_data
            # return d94_get_historical_data(
            #     instrument_token=instrument_token,
            #     from_date=from_date,
            #     to_date=to_date,
            #     interval=interval
            # ).get('data', [])
            return []
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return []
    
    async def place_gtt_order(self, **kwargs: Any) -> Dict[str, Any]:
        """Place a Good Till Triggered (GTT) order"""
        try:
            # Placeholder implementation - in real environment, this would use d94_place_gtt_order
            # return d94_place_gtt_order(**kwargs)
            return {"status": "success", "message": "GTT order placement simulated"}
        except Exception as e:
            logger.error(f"Error placing GTT order: {e}")
            return {"error": str(e)}
    
    async def get_gtt_orders(self) -> List[Dict[str, Any]]:
        """Get all GTT orders"""
        try:
            # Placeholder implementation - in real environment, this would use d94_get_gtts
            # return d94_get_gtts().get('data', [])
            return []
        except Exception as e:
            logger.error(f"Error fetching GTT orders: {e}")
            return []
    
    async def analyze_market_data(self, instruments: List[str]) -> Dict[str, Any]:
        """Analyze market data for given instruments"""
        try:
            quotes = await self.get_live_quotes(instruments)
            analysis: Dict[str, Any] = {}
            
            for instrument, data in quotes.items():
                if isinstance(data, dict):
                    analysis[instrument] = {
                        'current_price': data.get('last_price', 0),
                        'change': data.get('net_change', 0),
                        'change_percent': data.get('change_percent', 0),
                        'volume': data.get('volume', 0),
                        'high': data.get('ohlc', {}).get('high', 0),
                        'low': data.get('ohlc', {}).get('low', 0),
                        'open': data.get('ohlc', {}).get('open', 0),
                        'close': data.get('ohlc', {}).get('close', 0),
                        'recommendation': self._generate_recommendation(data)
                    }
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing market data: {e}")
            return {}
    
    def _generate_recommendation(self, data: Dict[str, Any]) -> str:
        """Generate basic trading recommendation based on price data"""
        try:
            change_percent = float(data.get('change_percent', 0) or 0)
            volume = int(data.get('volume', 0) or 0)
            
            if change_percent > 5 and volume > 100000:
                return "Strong Bullish - High volume with significant price increase"
            elif change_percent > 2:
                return "Bullish - Positive momentum"
            elif change_percent < -5 and volume > 100000:
                return "Strong Bearish - High volume with significant price decrease"
            elif change_percent < -2:
                return "Bearish - Negative momentum"
            else:
                return "Neutral - Sideways movement"
        except Exception:
            return "Insufficient data for recommendation"

# Create the main agent instance
zerodha_agent = ZerodhaAgent()

# Create a simple agent wrapper for backward compatibility
class SimpleAgent:
    def __init__(self, model: str, name: str, description: str, instruction: str):
        self.model = model
        self.name = name
        self.description = description
        self.instruction = instruction

# Backward compatibility
root_agent = SimpleAgent(
    model='gemini-2.0-flash-001',
    name='zerodha_trading_agent',
    description='An AI agent for Zerodha trading operations',
    instruction='Assist users with trading operations on Zerodha platform'
)

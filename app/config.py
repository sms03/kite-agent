"""
Configuration settings for the Zerodha AI Agent
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for the Zerodha AI Agent"""
    
    # API Configuration
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 1  # seconds
    
    # Trading Configuration
    DEFAULT_EXCHANGE = "NSE"
    DEFAULT_PRODUCT = "CNC"
    DEFAULT_VALIDITY = "DAY"
    DEFAULT_ORDER_TYPE = "LIMIT"
    
    # Risk Management
    MAX_ORDER_VALUE = 100000  # Maximum order value without confirmation
    MAX_POSITION_SIZE = 0.1   # Maximum position size as % of portfolio
    STOP_LOSS_PERCENTAGE = 5  # Default stop loss percentage
    
    # Display Configuration
    PORTFOLIO_REFRESH_INTERVAL = 30  # seconds
    MARKET_DATA_REFRESH_INTERVAL = 5  # seconds
    MAX_DISPLAY_INSTRUMENTS = 20
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # AI Model Configuration
    MODEL_NAME = "gemini-2.0-flash-001"
    AGENT_NAME = "zerodha_trading_agent"
    
    # Market Hours (IST)
    MARKET_OPEN_TIME = "09:15"
    MARKET_CLOSE_TIME = "15:30"
    
    # Exchanges and their trading symbols format
    EXCHANGES = {
        "NSE": "National Stock Exchange",
        "BSE": "Bombay Stock Exchange", 
        "NFO": "NSE Futures & Options",
        "BFO": "BSE Futures & Options",
        "MCX": "Multi Commodity Exchange"
    }
    
    # Product types and descriptions
    PRODUCTS = {
        "CNC": "Cash and Carry (Delivery)",
        "MIS": "Margin Intraday Settlement",
        "NRML": "Normal (F&O)",
        "MTF": "Margin Trading Facility"
    }
    
    # Order types and descriptions
    ORDER_TYPES = {
        "MARKET": "Execute at current market price",
        "LIMIT": "Execute at specified price or better",
        "SL": "Stop Loss order with limit price",
        "SL-M": "Stop Loss Market order"
    }
    
    # Validity types
    VALIDITY_TYPES = {
        "DAY": "Valid for the trading day",
        "IOC": "Immediate or Cancel",
        "TTL": "Time Till Logout"
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as a dictionary"""
        return {
            attr: getattr(cls, attr)
            for attr in dir(cls)
            if not attr.startswith('_') and not callable(getattr(cls, attr))
        }
    
    @classmethod
    def validate_exchange(cls, exchange: str) -> bool:
        """Validate if exchange is supported"""
        return exchange.upper() in cls.EXCHANGES
    
    @classmethod
    def validate_product(cls, product: str) -> bool:
        """Validate if product type is supported"""
        return product.upper() in cls.PRODUCTS
    
    @classmethod
    def validate_order_type(cls, order_type: str) -> bool:
        """Validate if order type is supported"""
        return order_type.upper() in cls.ORDER_TYPES
    
    @classmethod
    def validate_validity(cls, validity: str) -> bool:
        """Validate if validity type is supported"""
        return validity.upper() in cls.VALIDITY_TYPES

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    MAX_ORDER_VALUE = 10000  # Lower limits for development

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = "INFO"
    MAX_ORDER_VALUE = 100000

class TestConfig(Config):
    """Test environment configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    MAX_ORDER_VALUE = 1000  # Very low limits for testing

# Get configuration based on environment
def get_config() -> Config:
    """Get configuration based on environment variable"""
    env = os.getenv('ZERODHA_ENV', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'test':
        return TestConfig()
    else:
        return DevelopmentConfig()

# Global configuration instance
config = get_config()

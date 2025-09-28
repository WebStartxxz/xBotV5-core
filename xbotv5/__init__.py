"""xBotV5 Core Framework - Professional Trading Bot Engine

A comprehensive framework for building sophisticated trading bots
with advanced features like AI integration, multi-exchange support,
and robust risk management.

Example:
    >>> from xbotv5 import Bot, Signal, Context
    >>> from xbotv5.indicators import RSI
    >>>
    >>> class MyBot(Bot):
    ...     def setup(self):
    ...         self.rsi = RSI(14)
    ...
    ...     async def on_candle(self, context):
    ...         rsi_value = await self.rsi.calculate(context.candles)
    ...         if rsi_value < 30:
    ...             return Signal.BUY
    ...         elif rsi_value > 70:
    ...             return Signal.SELL
    ...         return Signal.HOLD
    >>>
    >>> bot = MyBot()
    >>> bot.run()

For more information, see: https://github.com/WebStartxxz/xBotV5-core
"""

__version__ = "1.0.0"
__author__ = "WebStartxxz Team"
__email__ = "team@webstartxxz.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024 WebStartxxz"
__description__ = "Professional Trading Bot Framework"
__url__ = "https://github.com/WebStartxxz/xBotV5-core"

# Core imports
from .core.bot import Bot
from .core.strategy import BaseStrategy, Strategy
from .core.signal import Signal, SignalType
from .core.context import Context, MarketData
from .core.order import Order, OrderType, OrderStatus
from .core.position import Position
from .core.portfolio import Portfolio

# Event system
from .events import EventBus, Event

# Exceptions
from .exceptions import (
    XBotV5Exception,
    ConfigurationError,
    ExchangeError,
    StrategyError,
    RiskManagementError,
    InsufficientFundsError,
    OrderError
)

# Configuration
from .config import Config

# Utilities
from .utils import Logger, Formatter

# Main application class
from .app import App

# Public API
__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
    "__description__",
    "__url__",
    
    # Core classes
    "Bot",
    "BaseStrategy",
    "Strategy",
    "Signal",
    "SignalType",
    "Context",
    "MarketData",
    "Order",
    "OrderType", 
    "OrderStatus",
    "Position",
    "Portfolio",
    
    # Event system
    "EventBus",
    "Event",
    
    # Exceptions
    "XBotV5Exception",
    "ConfigurationError",
    "ExchangeError",
    "StrategyError",
    "RiskManagementError",
    "InsufficientFundsError",
    "OrderError",
    
    # Configuration
    "Config",
    
    # Utilities
    "Logger",
    "Formatter",
    
    # Application
    "App"
]
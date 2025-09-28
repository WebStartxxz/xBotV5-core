"""xBotV5 Core Module

This module contains the core components of the xBotV5 framework:
- Bot base class and lifecycle management
- Trading strategies and signal generation
- Market context and data structures
- Order and position management
- Portfolio tracking and analysis
"""

from .bot import Bot
from .strategy import BaseStrategy, Strategy
from .signal import Signal, SignalType
from .context import Context, MarketData
from .order import Order, OrderType, OrderStatus
from .position import Position
from .portfolio import Portfolio

__all__ = [
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
    "Portfolio"
]
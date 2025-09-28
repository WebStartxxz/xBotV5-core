"""Bot Base Class

This module defines the Bot base class that all trading bots inherit from.
It provides the core functionality for bot lifecycle management, event handling,
and trading operations.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from .signal import Signal, SignalType
from .context import Context
from .order import Order
from .position import Position
from .portfolio import Portfolio
from ..events import EventBus, Event
from ..exceptions import XBotV5Exception, ConfigurationError
from ..config import Config
from ..utils import Logger


class Bot(ABC):
    """Base class for all trading bots
    
    This abstract base class provides the framework for creating trading bots.
    All custom bots should inherit from this class and implement the required
    abstract methods.
    
    Attributes:
        name (str): Bot name identifier
        version (str): Bot version
        pairs (List[str]): Trading pairs the bot operates on
        timeframe (str): Timeframe for candle data (e.g., '1h', '15m')
        config (Dict[str, Any]): Bot configuration
        logger (logging.Logger): Bot logger instance
        event_bus (EventBus): Event bus for bot communication
        portfolio (Portfolio): Portfolio manager
        positions (Dict[str, Position]): Current positions by symbol
        orders (Dict[str, Order]): Active orders by ID
        
    Example:
        >>> class MyBot(Bot):
        ...     def setup(self):
        ...         self.name = "RSI Bot"
        ...         self.pairs = ["BTC/USDT"]
        ...
        ...     async def on_candle(self, context):
        ...         # Trading logic here
        ...         return Signal.HOLD
        >>>
        >>> bot = MyBot()
        >>> bot.run()
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the bot
        
        Args:
            config: Optional configuration dictionary
        """
        # Basic attributes
        self.name: str = "Unnamed Bot"
        self.version: str = "1.0.0"
        self.description: str = "A trading bot built with xBotV5"
        self.author: str = "Unknown"
        
        # Trading configuration
        self.pairs: List[str] = []
        self.timeframe: str = "1h"
        self.exchange: Optional[str] = None
        
        # Configuration
        self.config = Config(config or {})
        
        # Runtime state
        self._running: bool = False
        self._initialized: bool = False
        self._start_time: Optional[datetime] = None
        
        # Core components
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.event_bus = EventBus()
        self.portfolio = Portfolio()
        self.positions: Dict[str, Position] = {}
        self.orders: Dict[str, Order] = {}
        
        # Statistics
        self.total_trades: int = 0
        self.winning_trades: int = 0
        self.losing_trades: int = 0
        self.total_pnl: float = 0.0
        
        # Setup event handlers
        self._setup_event_handlers()
    
    @abstractmethod
    def setup(self) -> None:
        """Configure bot settings and indicators
        
        This method is called once during bot initialization.
        Override this method to configure your bot's settings,
        indicators, and any other initialization logic.
        
        Example:
            >>> def setup(self):
            ...     self.name = "My Trading Bot"
            ...     self.pairs = ["BTC/USDT", "ETH/USDT"]
            ...     self.timeframe = "15m"
            ...     self.rsi = RSI(period=14)
        """
        pass
    
    @abstractmethod
    async def on_start(self) -> None:
        """Called when bot starts
        
        This method is called when the bot begins execution.
        Use this for any async initialization that needs to happen
        at startup.
        
        Example:
            >>> async def on_start(self):
            ...     self.logger.info(f"Starting {self.name}")
            ...     await self.exchange.connect()
        """
        pass
    
    @abstractmethod
    async def on_candle(self, context: Context) -> Signal:
        """Main trading logic - called on each new candle
        
        This is the core method where you implement your trading strategy.
        It's called every time a new candle is received for the configured
        timeframe and trading pairs.
        
        Args:
            context: Market context with candle data, indicators, etc.
            
        Returns:
            Signal: Trading signal (BUY, SELL, or HOLD)
            
        Example:
            >>> async def on_candle(self, context):
            ...     rsi = await self.rsi.calculate(context.candles)
            ...     if rsi < 30:
            ...         return Signal.BUY
            ...     elif rsi > 70:
            ...         return Signal.SELL
            ...     return Signal.HOLD
        """
        pass
    
    async def on_tick(self, context: Context) -> Optional[Signal]:
        """Called on each price tick (optional)
        
        Override this method if you need to react to individual
        price ticks rather than just candle closes.
        
        Args:
            context: Market context with tick data
            
        Returns:
            Optional[Signal]: Trading signal or None
        """
        return None
    
    @abstractmethod
    async def on_order_filled(self, order: Order) -> None:
        """Called when an order is filled
        
        This method is called whenever one of the bot's orders
        gets executed by the exchange.
        
        Args:
            order: The filled order
            
        Example:
            >>> async def on_order_filled(self, order):
            ...     self.logger.info(f"Order filled: {order}")
            ...     if order.side == "buy":
            ...         await self.set_stop_loss(order.symbol, order.price * 0.98)
        """
        pass
    
    @abstractmethod
    async def on_error(self, error: Exception) -> None:
        """Error handler
        
        This method is called when an error occurs during bot execution.
        Use this to implement custom error handling, logging, and recovery.
        
        Args:
            error: The exception that occurred
            
        Example:
            >>> async def on_error(self, error):
            ...     self.logger.error(f"Bot error: {error}")
            ...     if isinstance(error, ConnectionError):
            ...         await self.reconnect()
        """
        pass
    
    @abstractmethod
    async def on_stop(self) -> None:
        """Cleanup when bot stops
        
        This method is called when the bot is stopping.
        Use this for cleanup operations, closing connections,
        and saving state.
        
        Example:
            >>> async def on_stop(self):
            ...     self.logger.info(f"Stopping {self.name}")
            ...     await self.close_all_positions()
            ...     await self.exchange.disconnect()
        """
        pass
    
    def _setup_event_handlers(self) -> None:
        """Setup internal event handlers"""
        self.event_bus.on("order_filled", self._handle_order_filled)
        self.event_bus.on("position_opened", self._handle_position_opened)
        self.event_bus.on("position_closed", self._handle_position_closed)
        self.event_bus.on("error", self._handle_error)
    
    async def _handle_order_filled(self, event: Event) -> None:
        """Handle order filled event"""
        order = event.data.get("order")
        if order:
            await self.on_order_filled(order)
            self.total_trades += 1
    
    async def _handle_position_opened(self, event: Event) -> None:
        """Handle position opened event"""
        position = event.data.get("position")
        if position:
            self.positions[position.symbol] = position
            self.logger.info(f"Position opened: {position}")
    
    async def _handle_position_closed(self, event: Event) -> None:
        """Handle position closed event"""
        position = event.data.get("position")
        if position:
            # Update statistics
            if position.pnl > 0:
                self.winning_trades += 1
            else:
                self.losing_trades += 1
            
            self.total_pnl += position.pnl
            
            # Remove from positions
            if position.symbol in self.positions:
                del self.positions[position.symbol]
            
            self.logger.info(f"Position closed: {position}")
    
    async def _handle_error(self, event: Event) -> None:
        """Handle error event"""
        error = event.data.get("error")
        if error:
            await self.on_error(error)
    
    async def initialize(self) -> None:
        """Initialize the bot"""
        if self._initialized:
            return
        
        try:
            # Run user setup
            self.setup()
            
            # Validate configuration
            self._validate_config()
            
            # Mark as initialized
            self._initialized = True
            
            self.logger.info(f"Bot {self.name} v{self.version} initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize bot: {e}")
            raise ConfigurationError(f"Bot initialization failed: {e}")
    
    def _validate_config(self) -> None:
        """Validate bot configuration"""
        if not self.name:
            raise ConfigurationError("Bot name is required")
        
        if not self.pairs:
            raise ConfigurationError("At least one trading pair is required")
        
        if not self.timeframe:
            raise ConfigurationError("Timeframe is required")
    
    async def run(self) -> None:
        """Main bot loop
        
        This method starts the bot and runs the main trading loop.
        It handles initialization, event processing, and cleanup.
        
        Example:
            >>> bot = MyBot()
            >>> await bot.run()  # Or bot.run() in sync context
        """
        if not self._initialized:
            await self.initialize()
        
        self._running = True
        self._start_time = datetime.utcnow()
        
        self.logger.info(f"Starting bot {self.name}")
        
        try:
            # Call user's on_start method
            await self.on_start()
            
            # Emit start event
            await self.event_bus.emit("bot_started", {"bot": self})
            
            # Main trading loop
            while self._running:
                try:
                    # Process market data and trading logic
                    await self._process_market_data()
                    
                    # Small delay to prevent excessive CPU usage
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    self.logger.error(f"Error in trading loop: {e}")
                    await self.event_bus.emit("error", {"error": e})
                    
                    # Continue running unless it's a critical error
                    if isinstance(e, (KeyboardInterrupt, SystemExit)):
                        break
        
        except Exception as e:
            self.logger.error(f"Fatal error in bot: {e}")
            await self.event_bus.emit("error", {"error": e})
        
        finally:
            # Cleanup
            await self._cleanup()
    
    async def _process_market_data(self) -> None:
        """Process market data and execute trading logic"""
        # This would be implemented to fetch market data
        # and call the user's on_candle method
        # For now, it's a placeholder
        pass
    
    async def stop(self) -> None:
        """Stop the bot"""
        self.logger.info(f"Stopping bot {self.name}")
        self._running = False
    
    async def _cleanup(self) -> None:
        """Cleanup when bot stops"""
        try:
            # Call user's cleanup method
            await self.on_stop()
            
            # Emit stop event
            await self.event_bus.emit("bot_stopped", {"bot": self})
            
            self.logger.info(f"Bot {self.name} stopped")
        
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def has_position(self, symbol: Optional[str] = None) -> bool:
        """Check if bot has position(s)
        
        Args:
            symbol: Optional symbol to check. If None, checks any position.
            
        Returns:
            bool: True if position exists
        """
        if symbol:
            return symbol in self.positions
        return len(self.positions) > 0
    
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for symbol
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Optional[Position]: Position if exists, None otherwise
        """
        return self.positions.get(symbol)
    
    @property
    def is_running(self) -> bool:
        """Check if bot is running"""
        return self._running
    
    @property
    def uptime(self) -> Optional[float]:
        """Get bot uptime in seconds"""
        if self._start_time:
            return (datetime.utcnow() - self._start_time).total_seconds()
        return None
    
    @property
    def win_rate(self) -> float:
        """Calculate win rate percentage"""
        total = self.winning_trades + self.losing_trades
        if total == 0:
            return 0.0
        return (self.winning_trades / total) * 100
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get bot trading statistics
        
        Returns:
            Dict with bot performance metrics
        """
        return {
            "name": self.name,
            "version": self.version,
            "uptime": self.uptime,
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": self.win_rate,
            "total_pnl": self.total_pnl,
            "active_positions": len(self.positions),
            "active_orders": len(self.orders),
            "pairs": self.pairs,
            "timeframe": self.timeframe
        }
    
    def __str__(self) -> str:
        return f"Bot(name={self.name}, version={self.version}, pairs={self.pairs})"
    
    def __repr__(self) -> str:
        return self.__str__()
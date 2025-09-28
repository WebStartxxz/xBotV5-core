"""Trading Signal Classes

This module defines the Signal and SignalType classes used throughout
the xBotV5 framework to represent trading decisions and actions.
"""

from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


class SignalType(Enum):
    """Enumeration of trading signal types
    
    Attributes:
        BUY: Signal to open a long position
        SELL: Signal to close a long position or open a short position
        HOLD: Signal to maintain current position
        CLOSE: Signal to close current position
        STOP_LOSS: Signal triggered by stop loss
        TAKE_PROFIT: Signal triggered by take profit
    """
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    CLOSE = "close"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"


@dataclass
class Signal:
    """Trading signal with metadata
    
    A signal represents a trading decision made by a bot or strategy.
    It includes the signal type, confidence level, and optional metadata.
    
    Attributes:
        type (SignalType): The type of signal
        symbol (str): Trading pair symbol
        confidence (float): Confidence level (0.0 to 1.0)
        price (Optional[float]): Suggested execution price
        quantity (Optional[float]): Suggested position size
        stop_loss (Optional[float]): Stop loss price
        take_profit (Optional[float]): Take profit price
        metadata (Dict[str, Any]): Additional signal metadata
        timestamp (datetime): When signal was generated
        source (str): Source of the signal (bot/strategy name)
        
    Example:
        >>> signal = Signal(
        ...     type=SignalType.BUY,
        ...     symbol="BTC/USDT",
        ...     confidence=0.85,
        ...     price=45000.0,
        ...     stop_loss=44000.0,
        ...     take_profit=46000.0
        ... )
    """
    type: SignalType
    symbol: str
    confidence: float = 1.0
    price: Optional[float] = None
    quantity: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = None
    source: str = "unknown"
    
    def __post_init__(self):
        """Post-initialization processing"""
        if self.metadata is None:
            self.metadata = {}
        
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        
        # Validate confidence level
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
    
    @classmethod
    def buy(cls, symbol: str, **kwargs) -> "Signal":
        """Create a BUY signal
        
        Args:
            symbol: Trading pair symbol
            **kwargs: Additional signal parameters
            
        Returns:
            Signal: BUY signal instance
        """
        return cls(type=SignalType.BUY, symbol=symbol, **kwargs)
    
    @classmethod
    def sell(cls, symbol: str, **kwargs) -> "Signal":
        """Create a SELL signal
        
        Args:
            symbol: Trading pair symbol
            **kwargs: Additional signal parameters
            
        Returns:
            Signal: SELL signal instance
        """
        return cls(type=SignalType.SELL, symbol=symbol, **kwargs)
    
    @classmethod
    def hold(cls, symbol: str, **kwargs) -> "Signal":
        """Create a HOLD signal
        
        Args:
            symbol: Trading pair symbol
            **kwargs: Additional signal parameters
            
        Returns:
            Signal: HOLD signal instance
        """
        return cls(type=SignalType.HOLD, symbol=symbol, **kwargs)
    
    @classmethod
    def close(cls, symbol: str, **kwargs) -> "Signal":
        """Create a CLOSE signal
        
        Args:
            symbol: Trading pair symbol
            **kwargs: Additional signal parameters
            
        Returns:
            Signal: CLOSE signal instance
        """
        return cls(type=SignalType.CLOSE, symbol=symbol, **kwargs)
    
    def is_actionable(self) -> bool:
        """Check if signal requires action
        
        Returns:
            bool: True if signal is not HOLD
        """
        return self.type != SignalType.HOLD
    
    def is_entry_signal(self) -> bool:
        """Check if signal is for entering a position
        
        Returns:
            bool: True if signal is BUY
        """
        return self.type == SignalType.BUY
    
    def is_exit_signal(self) -> bool:
        """Check if signal is for exiting a position
        
        Returns:
            bool: True if signal is SELL, CLOSE, STOP_LOSS, or TAKE_PROFIT
        """
        return self.type in {SignalType.SELL, SignalType.CLOSE, 
                           SignalType.STOP_LOSS, SignalType.TAKE_PROFIT}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert signal to dictionary
        
        Returns:
            Dict[str, Any]: Signal as dictionary
        """
        return {
            "type": self.type.value,
            "symbol": self.symbol,
            "confidence": self.confidence,
            "price": self.price,
            "quantity": self.quantity,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "source": self.source
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Signal":
        """Create signal from dictionary
        
        Args:
            data: Signal data as dictionary
            
        Returns:
            Signal: Signal instance
        """
        signal_data = data.copy()
        signal_data["type"] = SignalType(data["type"])
        
        if data.get("timestamp"):
            signal_data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        
        return cls(**signal_data)
    
    def __str__(self) -> str:
        return (f"Signal({self.type.value.upper()} {self.symbol} "
                f"confidence={self.confidence:.2f} price={self.price})")
    
    def __repr__(self) -> str:
        return self.__str__()


# Convenience constants for backward compatibility
class SignalConstants:
    """Signal constants for easy access"""
    BUY = SignalType.BUY
    SELL = SignalType.SELL
    HOLD = SignalType.HOLD
    CLOSE = SignalType.CLOSE
    STOP_LOSS = SignalType.STOP_LOSS
    TAKE_PROFIT = SignalType.TAKE_PROFIT


# Make constants available at module level
BUY = SignalType.BUY
SELL = SignalType.SELL
HOLD = SignalType.HOLD
CLOSE = SignalType.CLOSE
STOP_LOSS = SignalType.STOP_LOSS
TAKE_PROFIT = SignalType.TAKE_PROFIT
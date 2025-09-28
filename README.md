# xBotV5 Core Framework 🤖

<div align="center">

![Core Framework](https://img.shields.io/badge/xBotV5-Core-blue?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.11+-green?style=for-the-badge&logo=python)
![Trading](https://img.shields.io/badge/Trading-Engine-gold?style=for-the-badge&logo=chart-line)

**Professional Trading Bot Framework - Core Engine**

[🤖 Bots](#-bots) • [📈 Strategies](#-strategies) • [📊 Indicators](#-indicators) • [🔌 APIs](#-apis)

</div>

---

## 🎯 Overview

xBotV5-core é o coração do ecossistema xBotV5 - um framework profissional para desenvolvimento de bots de trading automatizados com suporte a múltiplas exchanges, estratégias avançadas e integração completa com IA.

## ✨ Features

### 🤖 Bot Engine
- **Lifecycle Management**: Controle completo do ciclo de vida dos bots
- **Event-Driven Architecture**: Sistema de eventos assíncronos
- **Multi-Exchange Support**: Binance, Coinbase, Kraken e mais
- **Real-time Processing**: Processamento de dados em tempo real
- **Error Recovery**: Sistema avançado de recuperação de erros

### 📈 Trading Strategies
- **Grid Trading**: Estratégias de grade automatizadas
- **DCA (Dollar Cost Averaging)**: Média de preços inteligente
- **Scalping**: Operações de alta frequência
- **Swing Trading**: Operações de médio prazo
- **Custom Strategies**: Framework para estratégias personalizadas

### 📊 Technical Analysis
- **50+ Indicators**: RSI, MACD, Bollinger Bands, Stochastic e mais
- **Custom Indicators**: Criação de indicadores personalizados
- **Pattern Recognition**: Reconhecimento de padrões gráficos
- **Market Analysis**: Análise automatizada de mercado

### 🧠 AI Integration
- **Gemini AI**: Análise de mercado com IA do Google
- **Market Sentiment**: Análise de sentimento de mercado
- **Predictive Models**: Modelos preditivos avançados
- **Risk Assessment**: Avaliação automatizada de risco

### 🔒 Risk Management
- **Position Sizing**: Cálculo automático de posições
- **Stop Loss**: Stops dinâmicos e trailing stops
- **Take Profit**: Múltiplos níveis de lucro
- **Drawdown Control**: Controle de drawdown máximo
- **Portfolio Protection**: Proteção de portfólio

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│             User Bots               │
├─────────────────────────────────────┤
│           xBotV5 Core               │
├──────────┬──────────┬───────────────┤
│   Bot    │ Strategy │   Indicators  │
│  Engine  │  System  │    System     │
├──────────┼──────────┼───────────────┤
│ Exchange │   Risk   │      AI       │
│   APIs   │ Manager  │   Analysis    │
└──────────┴──────────┴───────────────┘
```

### Core Components

- **🤖 Bot Engine**: Manages bot lifecycle and execution
- **📈 Strategy System**: Handles trading logic and decision making
- **📊 Indicator System**: Technical analysis and market data processing
- **🔌 Exchange Integration**: Multi-exchange connectivity
- **⚡ Event Bus**: Asynchronous event handling
- **🧠 AI Module**: Artificial intelligence integration
- **🔒 Risk Manager**: Risk control and portfolio protection
- **💾 Data Manager**: Market data storage and retrieval

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (coming soon)
pip install xbotv5-core

# Or install from source
git clone https://github.com/WebStartxxz/xBotV5-core.git
cd xBotV5-core
pip install -e .
```

### Your First Bot

```python
# my_first_bot.py
from xbotv5 import Bot, Signal, Context
from xbotv5.indicators import RSI

class MyFirstBot(Bot):
    """Simple RSI-based trading bot"""
    
    def setup(self):
        """Configure bot settings"""
        self.name = "My First Bot"
        self.pairs = ["BTC/USDT"]
        self.timeframe = "1h"
        
        # Setup indicators
        self.rsi = RSI(period=14)
        
        # Risk settings
        self.stop_loss = 0.02  # 2%
        self.take_profit = 0.05  # 5%
    
    async def on_candle(self, context: Context) -> Signal:
        """Main trading logic - called on each new candle"""
        # Calculate RSI
        rsi_value = await self.rsi.calculate(context.candles)
        
        # Trading logic
        if rsi_value < 30 and not self.has_position():
            return Signal.BUY
        elif rsi_value > 70 and self.has_position():
            return Signal.SELL
            
        return Signal.HOLD
    
    async def on_order_filled(self, order):
        """Called when order is executed"""
        self.log.info(f"Order filled: {order.symbol} - {order.side} - {order.quantity}")
        
        # Send notification
        if hasattr(self, 'telegram'):
            await self.telegram.send(f"🤖 Order Filled!\n{order}")

# Run the bot
if __name__ == "__main__":
    bot = MyFirstBot()
    bot.run()
```

### Configuration

```python
# config.py
BOT_CONFIG = {
    "exchange": "binance",
    "testnet": True,  # Always start with testnet!
    "capital": 1000,  # USDT
    "risk": {
        "max_position_size": 0.1,  # 10% of capital
        "max_drawdown": 0.2,       # 20% max drawdown
        "stop_loss": 0.02,         # 2% stop loss
        "take_profit": 0.05        # 5% take profit
    },
    "telegram": {
        "enabled": True,
        "token": "your-bot-token",
        "chat_id": "your-chat-id"
    }
}

bot = MyFirstBot(config=BOT_CONFIG)
bot.run()
```

---

## 🤖 Bots

### Bot Base Class

```python
from xbotv5 import Bot

class CustomBot(Bot):
    def setup(self):
        """Configure bot - called once on startup"""
        pass
    
    async def on_start(self):
        """Called when bot starts"""
        pass
    
    async def on_candle(self, context):
        """Main trading logic - called on each candle"""
        return Signal.HOLD
    
    async def on_tick(self, context):
        """Called on price ticks (optional)"""
        pass
    
    async def on_order_filled(self, order):
        """Called when order is filled"""
        pass
    
    async def on_error(self, error):
        """Error handling"""
        pass
    
    async def on_stop(self):
        """Cleanup when bot stops"""
        pass
```

### Advanced Bot Example

```python
from xbotv5 import Bot, Signal, Context
from xbotv5.indicators import RSI, MACD, BollingerBands
from xbotv5.ai import GeminiAI

class AITradingBot(Bot):
    """AI-powered trading bot with advanced risk management"""
    
    def setup(self):
        self.name = "AI Trader Pro"
        self.pairs = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
        self.timeframe = "15m"
        
        # Technical indicators
        self.rsi = RSI(14)
        self.macd = MACD(12, 26, 9)
        self.bb = BollingerBands(20, 2)
        
        # AI integration
        self.ai = GeminiAI(model="gemini-pro")
        
        # Risk management
        self.max_positions = 3
        self.risk_per_trade = 0.02  # 2% per trade
        
    async def on_candle(self, context: Context) -> Signal:
        """AI-enhanced trading logic"""
        # Get technical analysis
        rsi = await self.rsi.calculate(context.candles)
        macd_line, signal_line, histogram = await self.macd.calculate(context.candles)
        upper_band, middle_band, lower_band = await self.bb.calculate(context.candles)
        
        # Get AI market analysis
        ai_analysis = await self.ai.analyze_market(
            candles=context.candles[-100:],  # Last 100 candles
            indicators={
                "rsi": rsi,
                "macd": {"line": macd_line, "signal": signal_line},
                "bollinger": {"upper": upper_band, "lower": lower_band}
            },
            news=context.news,
            sentiment=context.market_sentiment
        )
        
        # Combine technical and AI analysis
        technical_score = self._calculate_technical_score(rsi, macd_line, signal_line)
        ai_score = ai_analysis.confidence * ai_analysis.direction
        
        final_score = (technical_score * 0.6) + (ai_score * 0.4)
        
        # Risk management check
        if len(self.positions) >= self.max_positions:
            return Signal.HOLD
            
        # Trading decision
        if final_score > 0.7 and not self.has_position(context.symbol):
            return Signal.BUY
        elif final_score < -0.7 and self.has_position(context.symbol):
            return Signal.SELL
            
        return Signal.HOLD
    
    def _calculate_technical_score(self, rsi, macd_line, signal_line):
        """Calculate technical analysis score"""
        score = 0
        
        # RSI analysis
        if rsi < 30:
            score += 0.5  # Oversold
        elif rsi > 70:
            score -= 0.5  # Overbought
            
        # MACD analysis
        if macd_line > signal_line:
            score += 0.3  # Bullish
        else:
            score -= 0.3  # Bearish
            
        return score
```

---

## 📈 Strategies

### Grid Trading Strategy

```python
from xbotv5.strategies import GridStrategy

class MyGridBot(Bot):
    def setup(self):
        self.strategy = GridStrategy(
            grid_size=10,        # Number of grid levels
            grid_spacing=0.005,  # 0.5% spacing between levels
            base_order_size=100, # Base order size in USDT
            profit_per_grid=0.01 # 1% profit per grid level
        )
    
    async def on_candle(self, context):
        return await self.strategy.analyze(context)
```

### DCA Strategy

```python
from xbotv5.strategies import DCAStrategy

class MyDCABot(Bot):
    def setup(self):
        self.strategy = DCAStrategy(
            base_order=50,           # Initial order size
            safety_orders=5,         # Number of safety orders
            safety_order_size=100,   # Size of each safety order
            safety_order_step=2.5,   # % drop for safety orders
            take_profit=1.5          # % profit target
        )
```

---

## 📊 Indicators

### Built-in Indicators

```python
from xbotv5.indicators import (
    # Trend Indicators
    SMA, EMA, WMA, VWMA,
    
    # Momentum Indicators  
    RSI, Stochastic, Williams,
    
    # Volatility Indicators
    BollingerBands, ATR, Keltner,
    
    # Volume Indicators
    OBV, VWAP, MFI,
    
    # Oscillators
    MACD, CCI, ROC
)

# Usage example
rsi = RSI(period=14)
macd = MACD(fast=12, slow=26, signal=9)
bb = BollingerBands(period=20, std_dev=2)

# In your bot
async def on_candle(self, context):
    rsi_value = await self.rsi.calculate(context.candles)
    macd_line, signal_line, histogram = await self.macd.calculate(context.candles)
    upper, middle, lower = await self.bb.calculate(context.candles)
```

### Custom Indicators

```python
from xbotv5.indicators.base import BaseIndicator

class CustomRSI(BaseIndicator):
    """Custom RSI implementation with additional features"""
    
    def __init__(self, period=14, overbought=70, oversold=30):
        super().__init__()
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
    
    async def calculate(self, candles):
        # Your custom calculation logic
        rsi = self._calculate_rsi(candles)
        
        # Add custom logic
        signal = "neutral"
        if rsi > self.overbought:
            signal = "sell"
        elif rsi < self.oversold:
            signal = "buy"
            
        return {
            "rsi": rsi,
            "signal": signal,
            "strength": abs(rsi - 50) / 50
        }
```

---

## 🔌 APIs

### REST API

```python
# Start API server
from xbotv5.api import APIServer

api = APIServer(port=8000)
api.add_bot(my_bot)
api.start()
```

### WebSocket API

```python
# Real-time data streaming
from xbotv5.websocket import WebSocketServer

ws = WebSocketServer(port=8001)
ws.stream_bot_data(my_bot)
ws.start()
```

---

## 🧪 Testing

### Backtesting

```python
from xbotv5.backtesting import Backtester

# Create backtester
backtester = Backtester(
    start_date="2024-01-01",
    end_date="2024-12-31",
    initial_capital=10000,
    commission=0.001  # 0.1% commission
)

# Add your bot
backtester.add_bot(MyBot())

# Run backtest
results = await backtester.run()

print(f"Total Return: {results.total_return:.2%}")
print(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
print(f"Max Drawdown: {results.max_drawdown:.2%}")
print(f"Win Rate: {results.win_rate:.2%}")
```

### Paper Trading

```python
from xbotv5.paper_trading import PaperTrader

# Paper trading (simulation with real data)
trader = PaperTrader(
    initial_capital=10000,
    exchange="binance"
)

bot = MyBot()
bot.set_trader(trader)  # Use paper trading instead of real
bot.run()
```

---

## 📊 Performance Metrics

### Built-in Metrics

```python
# Get bot performance
stats = await bot.get_statistics()

print(f"""
🤖 Bot Performance Report
━━━━━━━━━━━━━━━━━━━━━━━━━
Total Trades: {stats.total_trades}
Win Rate: {stats.win_rate:.1%}
Total P&L: {stats.total_pnl:.2f} USDT
Sharpe Ratio: {stats.sharpe_ratio:.2f}
Max Drawdown: {stats.max_drawdown:.2%}
Profit Factor: {stats.profit_factor:.2f}
Uptime: {stats.uptime}
""")
```

### Custom Metrics

```python
class CustomMetrics:
    def __init__(self, bot):
        self.bot = bot
    
    def calculate_custom_score(self):
        # Your custom performance calculation
        return score
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Exchange API Keys
BINANCE_API_KEY=your_api_key
BINANCE_SECRET=your_secret
BINANCE_TESTNET=true

# Database
DATABASE_URL=postgresql://user:pass@localhost/xbotv5
REDIS_URL=redis://localhost:6379

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# AI
GEMINI_API_KEY=your_gemini_key

# Logging
LOG_LEVEL=INFO
```

### Configuration File

```yaml
# config.yaml
bot:
  name: "My Trading Bot"
  version: "1.0.0"
  
exchange:
  name: "binance"
  testnet: true
  
trading:
  pairs: ["BTC/USDT", "ETH/USDT"]
  timeframe: "1h"
  capital: 1000
  
risk:
  max_position_size: 0.1
  stop_loss: 0.02
  take_profit: 0.05
  max_drawdown: 0.2
  
telegram:
  enabled: true
  notifications:
    trades: true
    errors: true
    daily_report: true
```

---

## 📚 Documentation

- [📖 Getting Started Guide](https://github.com/WebStartxxz/xBotV5-docs)
- [🔧 API Reference](https://github.com/WebStartxxz/xBotV5-docs/api-reference)
- [📈 Strategy Development](https://github.com/WebStartxxz/xBotV5-docs/strategies)
- [🧪 Testing & Backtesting](https://github.com/WebStartxxz/xBotV5-docs/testing)
- [🚀 Deployment Guide](https://github.com/WebStartxxz/xBotV5-devops)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](../CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## ⚠️ Disclaimer

Trading cryptocurrencies involves substantial risk and may not be suitable for everyone. Always:
- Start with paper trading
- Use testnet first
- Never invest more than you can afford to lose
- Understand the risks involved

---

<div align="center">

**🚀 Build the future of trading with xBotV5 Core!**

Made with ❤️ by [WebStartxxz](https://github.com/WebStartxxz)

</div>
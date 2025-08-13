# Contrarian Automated Trading System

A sophisticated automated trading system for MetaTrader 5 that implements a contrarian strategy with signal reversal, multi-timeframe analysis, and intelligent risk management.

## 🎯 Overview

This system takes traditional trading signals and reverses them for contrarian trading:
- **BUY signals** → Execute **SELL trades**
- **SELL signals** → Execute **BUY trades**

The system uses ATR-based dynamic stop loss and take profit calculations with ultra-strict signal filtering (7.0/10 minimum strength).

## ✨ Features

- **🔄 Contrarian Strategy**: Reverses all trading signals for contrarian approach
- **📊 Multi-Timeframe Analysis**: 1H, 4H, and Daily timeframe confluence
- **🎯 ATR-Based Risk Management**: Dynamic SL/TP using 1.5x ATR multipliers
- **📱 Telegram Notifications**: Real-time trade alerts and system status
- **🛡️ Ultra-Strict Filtering**: Only signals above 7.0/10 strength are executed
- **📈 7 Major Pairs**: EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD
- **⚡ One Trade Per Day**: Maximum 1 trade per symbol per day

## 📁 Project Structure

```
signal/
├── automated_trading_system.py    # Main trading engine
├── requirements.txt              # Python dependencies
├── README.md                    # This file
├── docs/                       # Documentation
├── src/                        # Source modules
│   ├── config.py              # Trading configuration
│   ├── signal_generator.py    # Signal analysis engine
│   ├── mt5_connector.py       # MetaTrader 5 interface
│   └── telegram_notifier.py   # Telegram notifications
└── tests/                     # Unit tests
```

## 🚀 Quick Start

### Prerequisites

1. **MetaTrader 5** installed and running
2. **Python 3.8+** with pip
3. **Telegram Bot** (optional, for notifications)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd signal
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables (optional):
```bash
# For Telegram notifications
set TELEGRAM_BOT_TOKEN=your_bot_token
set TELEGRAM_CHAT_ID=your_chat_id
set TELEGRAM_ENABLED=true
```

### Running the System

```bash
python automated_trading_system.py
```

## ⚙️ Configuration

### Core Settings (`src/config.py`)

```python
# Contrarian Strategy
REVERSE_SIGNALS = True  # Enable signal reversal

# Risk Management
SL_MULTIPLIER = 1.5    # Stop Loss: 1.5x ATR
TP_MULTIPLIER = 1.5    # Take Profit: 1.5x ATR (1:1 Risk/Reward)

# Signal Filtering
MIN_SIGNAL_STRENGTH = 7.0  # Ultra-strict filtering

# Trading Pairs
SYMBOLS = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'USDCAD', 'NZDUSD']
```

### MetaTrader 5 Setup

1. Enable algorithmic trading in MT5
2. Allow DLL imports in Expert Advisors settings
3. Ensure the trading account has sufficient margin

## 🔧 How It Works

### 1. Signal Generation
- Multi-timeframe technical analysis (1H, 4H, Daily)
- Confluence detection across multiple indicators
- Ultra-strict filtering (minimum 7.0/10 strength)

### 2. Contrarian Conversion
```python
if signal == "BUY":
    execute_trade("SELL")  # Contrarian reversal
elif signal == "SELL":
    execute_trade("BUY")   # Contrarian reversal
```

### 3. Risk Management
- **Stop Loss**: Entry ± (1.5 × ATR)
- **Take Profit**: Entry ± (1.5 × ATR)
- **Risk/Reward**: 1:1 ratio
- **Position Sizing**: Configurable lot size

### 4. Trade Execution
- Real-time market price execution
- Automatic SL/TP placement
- One trade per symbol per day limit
- Telegram notifications for all activities

## 📊 Technical Indicators Used

- **Moving Averages**: EMA 20, 50 confluence
- **RSI**: Overbought/oversold levels
- **MACD**: Trend confirmation
- **Bollinger Bands**: Volatility analysis
- **ATR**: Dynamic risk management
- **Support/Resistance**: Key level analysis

## 📱 Telegram Integration

Set up environment variables for notifications:

```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
TELEGRAM_ENABLED=true
```

### Notification Types:
- ✅ Trade execution alerts
- 📊 Signal generation updates
- 🔧 System status messages
- ⚠️ Error notifications

## 🛡️ Risk Warnings

**⚠️ Important Disclaimers:**

1. **High Risk**: Forex trading involves substantial risk of loss
2. **Contrarian Strategy**: This system trades against market trends
3. **No Guarantee**: Past performance doesn't guarantee future results
4. **Demo Testing**: Always test on demo accounts first
5. **Capital Risk**: Only trade with money you can afford to lose

## 🧪 Testing

Run unit tests:
```bash
python -m pytest tests/
```

Test Telegram notifications:
```bash
python src/telegram_notifier.py
```

## 📈 Performance Monitoring

The system provides detailed logging:
- Trade execution details
- Signal strength analysis
- Risk management metrics
- System performance statistics

## 🔄 Contrarian Strategy Details

### Why Contrarian?
- Markets often overshoot in both directions
- Strong signals can indicate exhaustion points
- Contrarian trades capture reversals at extremes

### Signal Reversal Logic:
- **BUY Signal Detected** → **SELL Trade Executed**
- **SELL Signal Detected** → **BUY Trade Executed**
- All SL/TP levels automatically adjusted for reversed direction

## 📞 Support

For issues or questions:
1. Check the logs for error details
2. Verify MT5 connection and settings
3. Ensure all dependencies are installed
4. Test with demo account first

## 📄 License

This project is for educational purposes. Please review and understand all risks before using with real capital.

---

**⚡ Ready to trade contrarian? The markets await your reversed signals!**

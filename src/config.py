#!/usr/bin/env python3
"""
Trading Configuration for Contrarian System

Central configuration with the EXACT settings that worked successfully.
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TradingConfig:
    """Trading Configuration Class - Exact working settings"""
    
    # ===== MT5 CONNECTION SETTINGS =====
    @staticmethod
    def _get_mt5_login():
        login_str = os.getenv('MT5_LOGIN', '248353032')
        if login_str.isdigit():
            return int(login_str)
        else:
            return 248353032  # Default value if placeholder used
    
    MT5_LOGIN = _get_mt5_login()
    MT5_PASSWORD = os.getenv('MT5_PASSWORD', '23235450Faouzi.')
    MT5_SERVER = os.getenv('MT5_SERVER', 'Exness-MT5Trial')
    
    # ===== CONTRARIAN STRATEGY SETTINGS =====
    
    # THIS IS THE KEY SETTING - ENABLES CONTRARIAN MODE
    REVERSE_SIGNALS = True          # ENABLED: BUY signals become SELL trades, SELL signals become BUY trades
    
    # Optimized Day Trading Timeframes
    PRIMARY_TIMEFRAME = 'M5'        # 5-minute primary for precise entries
    CONFIRMATION_TIMEFRAME = 'M15'  # 15-minute for entry confirmation
    TREND_TIMEFRAME = 'H1'          # 1-hour for trend confirmation
    BIAS_TIMEFRAME = 'H4'           # 4-hour for market bias
    
    # Trading Symbols (7 major pairs - exact list that worked)
    DEFAULT_SYMBOLS = [
        'EURUSDm', 'GBPUSDm', 'USDJPYm', 'USDCHFm', 
        'AUDUSDm', 'USDCADm', 'NZDUSDm'
    ]
    
    # ===== ULTRA-STRICT SIGNAL FILTERING =====
    
    # Signal Quality Requirements (Optimized for day trading)
    MIN_CONFLUENCES = 4             # Increased to 4 for better day trading signals
    MIN_SIGNAL_STRENGTH = 6.0       # Reduced to 6.0 for more opportunities in day trading
    
    # Technical Indicators (Optimized for day trading)
    TREND_MA_FAST = 20              # Fast EMA period (standard)
    TREND_MA_SLOW = 50              # Slow EMA period (standard)
    TREND_MA_FILTER = 100           # Filter EMA period
    
    ADX_PERIOD = 14                 # ADX calculation period
    ADX_TREND_THRESHOLD = 25        # Reduced for day trading (more opportunities)
    
    RSI_PERIOD = 14                 # RSI calculation period
    RSI_OVERSOLD = 25               # RSI oversold level (more sensitive)
    RSI_OVERBOUGHT = 75             # RSI overbought level (more sensitive)
    
    # ===== PROFESSIONAL RISK MANAGEMENT =====
    
    # Fixed Lot Size System
    FIXED_LOT_SIZE = 0.03           # Fixed 0.03 lot size per trade (=$3 risk)
    FIXED_RISK_AMOUNT = 3.0         # Fixed $3 risk per trade
    MAX_DAILY_DRAWDOWN = 70.0       # Maximum $70 daily loss
    
    # Position Management (Allow 7 concurrent trades)
    MAX_CONCURRENT_TRADES = 7       # Maximum 7 trades at a time (one per pair)
    MAX_TRADES_PER_DAY = 14         # Maximum 14 trades per day
    MAX_TRADES_PER_PAIR_PER_DAY = 2 # Maximum 2 trades per pair per day
    
    # Session-Based Trading Limits (1 trade per pair per session)
    MAX_LONDON_TRADES_PER_PAIR = 1  # 1 trade per pair during London session
    MAX_NY_TRADES_PER_PAIR = 1      # 1 trade per pair during NY session
    
    # Profit Targets and Limits
    DAILY_PROFIT_TARGET = 140.0     # Stop trading after $140 profit (14 × $10)
    STOP_TRADING_ON_PAIR_SUCCESS = True  # ENABLED: Stop trading pair after successful trade
    
    # Signal Priority System (Relaxed for day trading)
    PRIORITY_SIGNAL_THRESHOLD = 8.0 # Signals 8.0+ get absolute priority
    
    # Trade Following and Reversal Detection
    ENABLE_TRADE_FOLLOWING = True   # Monitor trades for major reversals
    REVERSAL_CHECK_INTERVAL = 30    # FASTER: Check for reversals every 30 seconds
    MAJOR_REVERSAL_THRESHOLD = 7.0  # REDUCED: Signal strength required for reversal
    REVERSAL_RSI_THRESHOLD = 30     # RSI threshold for reversal detection
    REVERSAL_CONFLUENCE_MIN = 3     # Minimum confluences for reversal signal
    
    # Dynamic Lot Size Calculation (Fixed at 0.03 lots)
    BASE_LOT_SIZE = 0.03            # Fixed lot size: 0.03 per trade
    
    # ===== ENHANCED ATR-BASED TP/SL SYSTEM =====
    ATR_PERIOD = 14                 # ATR calculation period
    
    # Optimized TP/SL for day trading (10 pips TP focus)
    SL_ATR_MULTIPLIER = 1.2         # Conservative stop loss: 1.2x ATR
    TP1_ATR_MULTIPLIER = 1.0        # REDUCED: 10 pips target ≈ 1.0x ATR
    TP2_ATR_MULTIPLIER = 2.0        # Secondary target: 2.0x ATR
    TP3_ATR_MULTIPLIER = 3.0        # Extended target: 3.0x ATR
    
    # Fixed pip targets (alternative to ATR)
    FIXED_TP_PIPS = 10              # Fixed 10 pip take profit
    FIXED_SL_PIPS = 15              # Fixed 15 pip stop loss
    USE_FIXED_PIPS = True           # Use fixed pips instead of ATR
    
    # Signal Strength Multipliers (adjusted for day trading)
    WEAK_SIGNAL_MULTIPLIER = 0.8    # For signals 5.0-6.9: reduce targets
    STRONG_SIGNAL_MULTIPLIER = 1.0  # For signals 7.0-7.9: standard targets  
    ULTRA_SIGNAL_MULTIPLIER = 1.2   # For signals 8.0-10.0: extend targets slightly
    
    # Multiple Take Profit System (optimized for day trading)
    TP1_CLOSE_PERCENT = 70          # Close 70% at TP1 (secure quick profits)
    TP2_CLOSE_PERCENT = 20          # Close 20% at TP2  
    TP3_CLOSE_PERCENT = 10          # Close 10% at TP3
    
    # Advanced Risk Management (optimized for day trading)
    BREAKEVEN_ENABLED = True        # Enable breakeven management
    BREAKEVEN_TRIGGER_PIPS = 5      # Move to BE when profit >= 5 pips
    TRAILING_STOP_ENABLED = True    # Enable trailing stop
    TRAILING_STOP_DISTANCE = 5      # Trail by 5 pips
    TRAILING_STOP_TRIGGER = 8       # Start trailing at 8 pips profit
    
    # Market Session Adjustments
    ASIAN_SESSION_MULTIPLIER = 0.7  # Reduce targets during Asian session
    LONDON_SESSION_MULTIPLIER = 1.2 # Extend targets during London session
    NY_SESSION_MULTIPLIER = 1.1     # Slight extension during NY session
    OVERLAP_SESSION_MULTIPLIER = 1.3 # Maximum extension during overlaps
    
    # ===== TIME MANAGEMENT =====
    
    # Trading Sessions (UTC Times)
    LONDON_SESSION_START = 8        # London session: 8 AM UTC
    LONDON_SESSION_END = 16         # London session: 4 PM UTC
    NY_SESSION_START = 13           # NY session: 1 PM UTC  
    NY_SESSION_END = 21             # NY session: 9 PM UTC
    
    # Trading Hours (Exact working schedule - UTC)
    TRADING_START_HOUR = 6          # Start at 6 AM UTC (London pre-market)
    TRADING_END_HOUR = 21           # End at 9 PM UTC (NY session end)
    
    # Daily Limits (Professional Risk Management)
    MAX_DAILY_LOSS = 20.0           # Stop trading if daily loss exceeds $20
    
    # ===== MARKET FILTERS =====
    
    # Volatility Requirements (Exact working thresholds)
    MIN_ATR_THRESHOLD = 0.0008      # Minimum ATR for trade execution
    MAX_SPREAD_MULTIPLIER = 1.5     # Maximum spread multiplier
    
    # Market Condition Requirements (Exact working filters)
    REQUIRE_TREND_ALIGNMENT = True  # Require multi-timeframe alignment
    REQUIRE_ADX_CONFIRMATION = True # Require ADX trend confirmation
    AVOID_CONSOLIDATION = True      # Avoid ranging markets
    
    # ===== TELEGRAM NOTIFICATIONS =====
    
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    TELEGRAM_ENABLED = os.getenv('TELEGRAM_ENABLED', 'False').lower() == 'true'
    
    # Notification Settings (All enabled for full transparency)
    NOTIFY_TRADE_ENTRIES = True     # Notify on trade entries
    NOTIFY_TRADE_EXITS = True       # Notify on trade exits
    NOTIFY_DAILY_SUMMARY = True     # Send daily summary
    NOTIFY_PROFIT_TARGETS = True    # Notify when TP/SL hit
    
    @classmethod
    def display_config(cls):
        """Display current configuration."""
        print("=== PROFESSIONAL CONTRARIAN TRADING SYSTEM ===")
        print(f"🎯 Strategy: {'CONTRARIAN (BUY→SELL, SELL→BUY)' if cls.REVERSE_SIGNALS else 'STANDARD'}")
        print(f"📊 Primary Timeframe: {cls.PRIMARY_TIMEFRAME}")
        print(f"💰 Fixed Lot Size: {cls.FIXED_LOT_SIZE} lots per trade (=$3 risk)")
        print(f"📈 Take Profit: {cls.TP1_ATR_MULTIPLIER}x, {cls.TP2_ATR_MULTIPLIER}x, {cls.TP3_ATR_MULTIPLIER}x ATR")
        print(f"🛑 Stop Loss: {cls.SL_ATR_MULTIPLIER}x ATR")
        print(f"🎯 Max Concurrent: {cls.MAX_CONCURRENT_TRADES} trades")
        print(f"🔍 Min Signal Strength: {cls.MIN_SIGNAL_STRENGTH}/10 ⭐ ULTRA-STRICT")
        print(f"📊 Trading Pairs: {len(cls.DEFAULT_SYMBOLS)}")
        print(f"⏰ Trading Hours: {cls.TRADING_START_HOUR}:00 - {cls.TRADING_END_HOUR}:00 UTC")
        print(f"� Max Daily Trades: {cls.MAX_TRADES_PER_DAY} ({cls.MAX_TRADES_PER_PAIR_PER_DAY} per pair)")
        print(f"🎯 Daily Profit Target: ${cls.DAILY_PROFIT_TARGET}")
        print(f"🔄 Trade Following: {'✅ ENABLED' if cls.ENABLE_TRADE_FOLLOWING else '❌ DISABLED'}")
        print("=" * 52)
    
    @classmethod
    def is_trading_hours(cls):
        """Check if current time is within trading hours."""
        current_hour = datetime.utcnow().hour
        return cls.TRADING_START_HOUR <= current_hour < cls.TRADING_END_HOUR
    
    @classmethod
    def get_trading_session_info(cls):
        """Get current trading session information."""
        current_hour = datetime.utcnow().hour
        
        if 0 <= current_hour < 6:
            return "ASIAN_SESSION", "Low volatility"
        elif 6 <= current_hour < 8:
            return "LONDON_PRE_MARKET", "Early London opportunities"
        elif 8 <= current_hour < 12:
            return "LONDON_SESSION", "High volatility - Prime time"
        elif 12 <= current_hour < 16:
            return "LONDON_NY_OVERLAP", "Highest volatility - Best time"
        elif 16 <= current_hour < 20:
            return "NY_SESSION", "Good volatility"
        else:
            return "QUIET_HOURS", "Low volatility"


# Legacy compatibility for any old imports
Config = TradingConfig
DayTradingConfig = TradingConfig

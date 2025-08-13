#!/usr/bin/env python3
"""
Test Day Trading Configuration

Test script to verify the new day trading optimizations.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import TradingConfig

def test_day_trading_config():
    """Test the day trading configuration."""
    print("🧪 TESTING DAY TRADING CONFIGURATION")
    print("=" * 50)
    
    # Display configuration
    TradingConfig.display_config()
    
    print("\n📊 DETAILED DAY TRADING SETTINGS:")
    print(f"Primary Timeframe: {TradingConfig.PRIMARY_TIMEFRAME}")
    print(f"Confirmation: {TradingConfig.CONFIRMATION_TIMEFRAME}")
    print(f"Trend: {TradingConfig.TREND_TIMEFRAME}")
    print(f"Bias: {TradingConfig.BIAS_TIMEFRAME}")
    
    print(f"\n🎯 PROFIT TARGETS:")
    if TradingConfig.USE_FIXED_PIPS:
        print(f"TP1: {TradingConfig.FIXED_TP_PIPS} pips (Fixed)")
        print(f"TP2: {TradingConfig.FIXED_TP_PIPS * 2} pips")
        print(f"TP3: {TradingConfig.FIXED_TP_PIPS * 3} pips")
        print(f"SL: {TradingConfig.FIXED_SL_PIPS} pips (Fixed)")
    else:
        print(f"TP1: {TradingConfig.TP1_ATR_MULTIPLIER}x ATR")
        print(f"TP2: {TradingConfig.TP2_ATR_MULTIPLIER}x ATR")
        print(f"TP3: {TradingConfig.TP3_ATR_MULTIPLIER}x ATR")
        print(f"SL: {TradingConfig.SL_ATR_MULTIPLIER}x ATR")
    
    print(f"\n🚀 POSITION MANAGEMENT:")
    print(f"Max Concurrent Trades: {TradingConfig.MAX_CONCURRENT_TRADES}")
    print(f"Max Trades Per Pair Per Day: {TradingConfig.MAX_TRADES_PER_PAIR_PER_DAY}")
    print(f"Max Daily Trades: {TradingConfig.MAX_TRADES_PER_DAY}")
    print(f"Daily Profit Target: ${TradingConfig.DAILY_PROFIT_TARGET}")
    print(f"Max Daily Drawdown: ${TradingConfig.MAX_DAILY_DRAWDOWN}")
    print(f"Stop After Success: {TradingConfig.STOP_TRADING_ON_PAIR_SUCCESS}")
    
    print(f"\n📅 SESSION-BASED TRADING:")
    print(f"London Session: {TradingConfig.LONDON_SESSION_START}:00 - {TradingConfig.LONDON_SESSION_END}:00 UTC")
    print(f"NY Session: {TradingConfig.NY_SESSION_START}:00 - {TradingConfig.NY_SESSION_END}:00 UTC")
    print(f"Max London Trades Per Pair: {TradingConfig.MAX_LONDON_TRADES_PER_PAIR}")
    print(f"Max NY Trades Per Pair: {TradingConfig.MAX_NY_TRADES_PER_PAIR}")
    
    print(f"\n⚡ SIGNAL REQUIREMENTS:")
    print(f"Min Signal Strength: {TradingConfig.MIN_SIGNAL_STRENGTH}/10")
    print(f"Min Confluences: {TradingConfig.MIN_CONFLUENCES}")
    print(f"RSI Overbought: {TradingConfig.RSI_OVERBOUGHT}")
    print(f"RSI Oversold: {TradingConfig.RSI_OVERSOLD}")
    print(f"ADX Threshold: {TradingConfig.ADX_TREND_THRESHOLD}")
    
    print(f"\n🔄 ADVANCED FEATURES:")
    print(f"Trade Following: {TradingConfig.ENABLE_TRADE_FOLLOWING}")
    print(f"Reversal Check Interval: {TradingConfig.REVERSAL_CHECK_INTERVAL}s")
    print(f"Breakeven Trigger: {TradingConfig.BREAKEVEN_TRIGGER_PIPS} pips")
    print(f"Trailing Stop: {TradingConfig.TRAILING_STOP_DISTANCE} pips")
    
    print("\n✅ DAY TRADING OPTIMIZATION VERIFICATION:")
    
    # Verify optimizations
    checks = []
    
    # Check timeframes
    if TradingConfig.PRIMARY_TIMEFRAME == 'M5':
        checks.append("✅ Primary timeframe set to M5 for precision")
    else:
        checks.append("❌ Primary timeframe should be M5")
    
    # Check TP target
    if TradingConfig.USE_FIXED_PIPS and TradingConfig.FIXED_TP_PIPS == 10:
        checks.append("✅ 10 pip TP target configured")
    else:
        checks.append("❌ 10 pip TP target not configured")
    
    # Check concurrent trades
    if TradingConfig.MAX_CONCURRENT_TRADES == 2:
        checks.append("✅ 2 concurrent trades (1 per session) enabled")
    else:
        checks.append("❌ Should allow 2 concurrent trades (1 per session)")
    
    # Check daily trades  
    if TradingConfig.MAX_TRADES_PER_DAY == 14:
        checks.append("✅ 14 daily trades (7 pairs × 2 sessions) configured")
    else:
        checks.append("❌ Should allow 14 daily trades")
    
    # Check stop after success
    if TradingConfig.STOP_TRADING_ON_PAIR_SUCCESS:
        checks.append("✅ Stop trading pair after success enabled")
    else:
        checks.append("❌ Should stop trading pair after success")
    
    # Check signal strength
    if TradingConfig.MIN_SIGNAL_STRENGTH <= 6.0:
        checks.append("✅ Signal strength relaxed for day trading")
    else:
        checks.append("❌ Signal strength too strict for day trading")
    
    # Check reversal speed
    if TradingConfig.REVERSAL_CHECK_INTERVAL <= 30:
        checks.append("✅ Fast reversal checking enabled")
    else:
        checks.append("❌ Reversal checking should be faster")
    
    for check in checks:
        print(check)
    
    print("\n🎯 PROFIT POTENTIAL CALCULATION:")
    profit_per_trade = TradingConfig.FIXED_TP_PIPS * 1.0  # Assuming $1 per pip
    max_daily_trades = TradingConfig.MAX_TRADES_PER_DAY
    theoretical_max_profit = max_daily_trades * profit_per_trade
    
    print(f"Session-based trading strategy:")
    print(f"  - London Session: 7 pairs × 1 trade = 7 trades max")
    print(f"  - NY Session: 7 pairs × 1 trade = 7 trades max") 
    print(f"  - Total: 14 trades max per day")
    print(f"Profit per trade: ${profit_per_trade:.2f} (10 pips)")
    print(f"Max daily trades: {max_daily_trades}")
    print(f"Theoretical max daily profit: ${theoretical_max_profit:.2f}")
    print(f"Configured daily target: ${TradingConfig.DAILY_PROFIT_TARGET}")
    print(f"Success strategy: Stop trading pair after first TP1 hit")
    
    print("\n=" * 50)
    print("🚀 DAY TRADING CONFIGURATION TEST COMPLETE!")

if __name__ == "__main__":
    test_day_trading_config()

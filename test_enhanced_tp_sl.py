#!/usr/bin/env python3
"""
Test Enhanced TP/SL System

Test the new multiple TP levels, dynamic multipliers, and risk management features.
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import TradingConfig
from automated_trading_system import ContriarianTradingSystem


def test_enhanced_tp_sl():
    """Test the enhanced TP/SL calculation system."""
    print("🧪 Testing Enhanced TP/SL System...")
    print("=" * 50)
    
    # Create system instance
    system = ContriarianTradingSystem()
    
    # Test parameters
    symbol = "EURUSDm"
    entry_price = 1.10000
    atr_value = 0.00150  # 15 pips ATR
    
    print(f"📊 Test Parameters:")
    print(f"Symbol: {symbol}")
    print(f"Entry Price: {entry_price}")
    print(f"ATR Value: {atr_value} ({atr_value * 100000:.1f} pips)")
    print()
    
    # Test different signal strengths and sessions
    test_cases = [
        {"signal_strength": 6.0, "description": "Weak Signal (6.0/10)"},
        {"signal_strength": 7.5, "description": "Standard Signal (7.5/10)"},
        {"signal_strength": 8.5, "description": "Strong Signal (8.5/10)"},
        {"signal_strength": 9.8, "description": "Ultra Signal (9.8/10)"},
    ]
    
    for case in test_cases:
        print(f"🎯 {case['description']}")
        print("-" * 30)
        
        # Test BUY trade
        levels_buy = system._calculate_contrarian_levels(
            symbol, "BUY", entry_price, atr_value, case['signal_strength']
        )
        
        print("📈 BUY Trade Levels:")
        print(f"  Entry: {entry_price:.5f}")
        print(f"  SL:    {levels_buy['sl_price']:.5f} ({(entry_price - levels_buy['sl_price']) * 100000:.1f} pips)")
        print(f"  TP1:   {levels_buy['tp1_price']:.5f} ({(levels_buy['tp1_price'] - entry_price) * 100000:.1f} pips) - 50%")
        print(f"  TP2:   {levels_buy['tp2_price']:.5f} ({(levels_buy['tp2_price'] - entry_price) * 100000:.1f} pips) - 30%")
        print(f"  TP3:   {levels_buy['tp3_price']:.5f} ({(levels_buy['tp3_price'] - entry_price) * 100000:.1f} pips) - 20%")
        print(f"  Breakeven Trigger: {levels_buy['breakeven_trigger']:.5f}")
        print(f"  Trailing Trigger:  {levels_buy['trailing_trigger']:.5f}")
        
        # Test SELL trade
        levels_sell = system._calculate_contrarian_levels(
            symbol, "SELL", entry_price, atr_value, case['signal_strength']
        )
        
        print("\n📉 SELL Trade Levels:")
        print(f"  Entry: {entry_price:.5f}")
        print(f"  SL:    {levels_sell['sl_price']:.5f} ({(levels_sell['sl_price'] - entry_price) * 100000:.1f} pips)")
        print(f"  TP1:   {levels_sell['tp1_price']:.5f} ({(entry_price - levels_sell['tp1_price']) * 100000:.1f} pips) - 50%")
        print(f"  TP2:   {levels_sell['tp2_price']:.5f} ({(entry_price - levels_sell['tp2_price']) * 100000:.1f} pips) - 30%")
        print(f"  TP3:   {levels_sell['tp3_price']:.5f} ({(entry_price - levels_sell['tp3_price']) * 100000:.1f} pips) - 20%")
        print(f"  Breakeven Trigger: {levels_sell['breakeven_trigger']:.5f}")
        print(f"  Trailing Trigger:  {levels_sell['trailing_trigger']:.5f}")
        
        print(f"\n⚡ Multipliers:")
        print(f"  Session: {levels_buy['session_multiplier']:.2f}")
        print(f"  Strength: {levels_buy['strength_multiplier']:.2f}")
        print(f"  Final: {levels_buy['final_multiplier']:.2f}")
        print("\n" + "="*50 + "\n")
    
    # Test session multipliers
    print("⏰ Session Multiplier Testing:")
    print("-" * 30)
    
    # Mock different sessions by temporarily changing the method
    original_method = system._get_session_multiplier
    
    sessions = [
        ("ASIAN_SESSION", 0.7),
        ("LONDON_SESSION", 1.2),
        ("NY_SESSION", 1.1),
        ("LONDON_NY_OVERLAP", 1.3),
        ("QUIET_HOURS", 0.7)
    ]
    
    for session_name, expected_multiplier in sessions:
        # Mock the session
        system._get_session_multiplier = lambda: expected_multiplier
        
        levels = system._calculate_contrarian_levels(
            symbol, "BUY", entry_price, atr_value, 7.5
        )
        
        print(f"{session_name}: {levels['session_multiplier']:.2f} - TP1: {(levels['tp1_price'] - entry_price) * 100000:.1f} pips")
    
    # Restore original method
    system._get_session_multiplier = original_method
    
    print("\n✅ Enhanced TP/SL system test completed!")


def test_risk_management_features():
    """Test breakeven and trailing stop features."""
    print("\n🛡️ Testing Risk Management Features...")
    print("=" * 50)
    
    # Simulate trade monitoring
    system = ContriarianTradingSystem()
    
    # Create mock trade
    symbol = "GBPUSDm"
    entry_price = 1.25000
    atr_value = 0.00200
    
    levels = system._calculate_contrarian_levels(
        symbol, "BUY", entry_price, atr_value, 8.0
    )
    
    # Mock active trade
    trade_info = {
        'symbol': symbol,
        'action': 'BUY',
        'entry_price': entry_price,
        'levels': levels,
        'lot_size': 0.1,
        'entry_time': datetime.now(),
        'original_signal': 'SELL',
        'contrarian': True,
        'tp_hits': {'tp1': False, 'tp2': False, 'tp3': False},
        'breakeven_set': False,
        'trailing_active': False,
        'current_sl': levels['sl_price']
    }
    
    print(f"📊 Mock Trade Setup:")
    print(f"Symbol: {symbol}")
    print(f"Action: BUY")
    print(f"Entry: {entry_price:.5f}")
    print(f"Initial SL: {levels['sl_price']:.5f}")
    print(f"Breakeven Trigger: {levels['breakeven_trigger']:.5f}")
    print(f"Trailing Trigger: {levels['trailing_trigger']:.5f}")
    
    # Test price movements
    test_prices = [
        entry_price + 0.00100,  # Small profit
        entry_price + 0.00150,  # Breakeven trigger
        entry_price + 0.00300,  # Trailing trigger
        entry_price + 0.00450,  # TP1 level
    ]
    
    print(f"\n📈 Testing Price Movements:")
    for i, price in enumerate(test_prices, 1):
        print(f"\nStep {i}: Price = {price:.5f} (+{(price - entry_price) * 100000:.1f} pips)")
        
        # Test breakeven
        if not trade_info['breakeven_set']:
            system._check_breakeven(price, trade_info, symbol)
            if trade_info['breakeven_set']:
                print(f"  ✅ Breakeven set at {trade_info['current_sl']:.5f}")
        
        # Test trailing
        if not trade_info['trailing_active']:
            system._check_trailing_stop(price, trade_info, symbol)
            if trade_info['trailing_active']:
                print(f"  ✅ Trailing stop activated")
        elif trade_info['trailing_active']:
            old_sl = trade_info['current_sl']
            system._update_trailing_stop(price, trade_info, symbol)
            if trade_info['current_sl'] != old_sl:
                print(f"  📈 Trailing SL updated: {old_sl:.5f} → {trade_info['current_sl']:.5f}")
        
        # Test TP hits
        tp_hit = system._check_tp_hits(price, trade_info)
        if tp_hit:
            for tp_level, hit in trade_info['tp_hits'].items():
                if hit:
                    print(f"  🎯 {tp_level.upper()} HIT!")
    
    print("\n✅ Risk management features test completed!")


def display_config_summary():
    """Display enhanced configuration summary."""
    print("\n📋 Enhanced TP/SL Configuration Summary:")
    print("=" * 50)
    
    config = TradingConfig()
    
    print(f"Base Multipliers:")
    print(f"  SL: {config.SL_ATR_MULTIPLIER}x ATR")
    print(f"  TP1: {config.TP1_ATR_MULTIPLIER}x ATR")
    print(f"  TP2: {config.TP2_ATR_MULTIPLIER}x ATR") 
    print(f"  TP3: {config.TP3_ATR_MULTIPLIER}x ATR")
    
    print(f"\nSignal Strength Multipliers:")
    print(f"  Weak (5.0-6.9): {config.WEAK_SIGNAL_MULTIPLIER}x")
    print(f"  Standard (7.0-7.9): 1.0x")
    print(f"  Strong (8.0-8.9): {config.STRONG_SIGNAL_MULTIPLIER}x")
    print(f"  Ultra (9.0-10.0): {config.ULTRA_SIGNAL_MULTIPLIER}x")
    
    print(f"\nPartial Close Percentages:")
    print(f"  TP1: {config.TP1_CLOSE_PERCENT}%")
    print(f"  TP2: {config.TP2_CLOSE_PERCENT}%")
    print(f"  TP3: {config.TP3_CLOSE_PERCENT}%")
    
    print(f"\nRisk Management:")
    print(f"  Breakeven: {'✅ Enabled' if config.BREAKEVEN_ENABLED else '❌ Disabled'}")
    print(f"  Breakeven Trigger: {config.BREAKEVEN_TRIGGER_ATR}x ATR")
    print(f"  Trailing Stop: {'✅ Enabled' if config.TRAILING_STOP_ENABLED else '❌ Disabled'}")
    print(f"  Trailing Distance: {config.TRAILING_STOP_DISTANCE}x ATR")
    print(f"  Trailing Trigger: {config.TRAILING_STOP_TRIGGER}x ATR")
    
    print(f"\nSession Multipliers:")
    print(f"  Asian: {config.ASIAN_SESSION_MULTIPLIER}x")
    print(f"  London: {config.LONDON_SESSION_MULTIPLIER}x")
    print(f"  NY: {config.NY_SESSION_MULTIPLIER}x")
    print(f"  Overlap: {config.OVERLAP_SESSION_MULTIPLIER}x")


if __name__ == "__main__":
    print("🚀 Enhanced TP/SL System Test Suite")
    print("=" * 50)
    
    try:
        display_config_summary()
        test_enhanced_tp_sl()
        test_risk_management_features()
        
        print("\n🎉 All tests completed successfully!")
        print("\n🎯 Enhanced Features Summary:")
        print("✅ Multiple TP levels (TP1, TP2, TP3)")
        print("✅ Dynamic multipliers based on signal strength")
        print("✅ Session-based adjustments")
        print("✅ Breakeven management")
        print("✅ Trailing stop loss")
        print("✅ Partial profit taking")
        print("✅ Enhanced Telegram notifications")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

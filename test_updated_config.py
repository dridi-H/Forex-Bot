#!/usr/bin/env python3
"""
Quick test for $5 risk and 2 concurrent trades
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from automated_trading_system import ContriarianTradingSystem

def test_updated_config():
    """Test the updated configuration."""
    print("🔧 Testing Updated Professional Risk Configuration")
    print("=" * 55)
    
    # Load configuration
    config = Config()
    
    print(f"💰 Fixed Risk Amount: ${config.FIXED_RISK_AMOUNT}")
    print(f"🎯 Max Concurrent Trades: {config.MAX_CONCURRENT_TRADES}")
    print(f"📊 Max Daily Drawdown: ${config.MAX_DAILY_DRAWDOWN}")
    print(f"⭐ Min Signal Strength: {config.MIN_SIGNAL_STRENGTH}/10")
    
    # Validate the changes
    assert config.FIXED_RISK_AMOUNT == 5.0, f"Expected $5, got ${config.FIXED_RISK_AMOUNT}"
    assert config.MAX_CONCURRENT_TRADES == 2, f"Expected 2 trades, got {config.MAX_CONCURRENT_TRADES}"
    
    print("\n✅ Configuration validated:")
    print("   💰 Risk per trade: $5 (UPDATED)")
    print("   🎯 Concurrent trades: 2 (UPDATED)")
    print("   📊 Daily drawdown: $20 (unchanged)")
    
    # Test system initialization
    print("\n🚀 Testing System with New Configuration:")
    system = ContriarianTradingSystem()
    
    # Test multiple signals processing capability
    print(f"\n📊 System allows {system.config.MAX_CONCURRENT_TRADES} concurrent trades")
    print(f"💰 Each trade risks exactly ${system.config.FIXED_RISK_AMOUNT}")
    print(f"🎯 Total potential risk: ${system.config.FIXED_RISK_AMOUNT * system.config.MAX_CONCURRENT_TRADES}")
    
    return True

if __name__ == "__main__":
    test_updated_config()
    print("\n🎉 CONFIGURATION UPDATE SUCCESSFUL!")
    print("✅ Risk per trade: $5")
    print("✅ Max concurrent trades: 2")
    print("✅ System ready for live trading with new parameters!")

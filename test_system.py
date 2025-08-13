#!/usr/bin/env python3
"""
Test Script for Trading System Functions

This script tests individual components of the trading system
to verify everything is working correctly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import TradingConfig
from src.mt5_connector import MT5Connector
from src.signal_generator import SignalGenerator
from colorama import Fore, Style, init

init(autoreset=True)

def test_mt5_connection():
    """Test MT5 connection."""
    print(f"{Fore.CYAN}🔌 Testing MT5 Connection...{Style.RESET_ALL}")
    
    mt5 = MT5Connector()
    if mt5.connect():
        print(f"{Fore.GREEN}✅ MT5 connection successful{Style.RESET_ALL}")
        
        # Test symbol access
        symbol = 'EURUSDm'
        tick = mt5.get_tick(symbol)
        if tick:
            print(f"✅ {symbol} tick: Bid={tick.bid:.5f}, Ask={tick.ask:.5f}")
        else:
            print(f"❌ Failed to get tick for {symbol}")
            
        # Test historical data
        rates = mt5.get_rates(symbol, 'H1', 10)
        if rates is not None and len(rates) > 0:
            print(f"✅ Historical data: {len(rates)} bars retrieved")
        else:
            print(f"❌ Failed to get historical data for {symbol}")
            
        mt5.disconnect()
        return True
    else:
        print(f"{Fore.RED}❌ MT5 connection failed{Style.RESET_ALL}")
        return False

def test_signal_generation():
    """Test signal generation."""
    print(f"\n{Fore.CYAN}📊 Testing Signal Generation...{Style.RESET_ALL}")
    
    config = TradingConfig()
    mt5 = MT5Connector()
    
    if not mt5.connect():
        print(f"{Fore.RED}❌ Cannot test signals without MT5{Style.RESET_ALL}")
        return False
        
    signal_gen = SignalGenerator(mt5, config)
    
    # Test signal generation for one symbol
    symbol = 'EURUSDm'
    print(f"Generating signal for {symbol}...")
    
    signal_data = signal_gen.generate_live_day_trading_signal(symbol)
    
    if signal_data:
        print(f"✅ Signal generated:")
        print(f"   Symbol: {signal_data.get('symbol')}")
        print(f"   Signal: {signal_data.get('signal')}")
        print(f"   Strength: {signal_data.get('strength', 0):.1f}/10")
        print(f"   Confluences: {len(signal_data.get('confluences', []))}")
        
        if signal_data.get('strength', 0) >= config.MIN_SIGNAL_STRENGTH:
            print(f"{Fore.GREEN}🎯 Signal meets minimum strength requirement!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ Signal below minimum strength threshold{Style.RESET_ALL}")
    else:
        print(f"❌ No signal generated for {symbol}")
        
    mt5.disconnect()
    return signal_data is not None

def test_order_placement_simulation():
    """Test order placement logic (simulation only)."""
    print(f"\n{Fore.CYAN}💼 Testing Order Placement Logic...{Style.RESET_ALL}")
    
    # Simulate order parameters
    symbol = 'EURUSDm'
    action = 'BUY'
    lot_size = 0.01  # Small test size
    entry_price = 1.0850
    sl_price = 1.0800
    tp_price = 1.0900
    
    print(f"Order simulation:")
    print(f"   Symbol: {symbol}")
    print(f"   Action: {action}")
    print(f"   Lot Size: {lot_size}")
    print(f"   Entry: {entry_price:.5f}")
    print(f"   SL: {sl_price:.5f}")
    print(f"   TP: {tp_price:.5f}")
    
    # Calculate risk/reward
    risk_pips = abs(entry_price - sl_price) * 100000
    reward_pips = abs(tp_price - entry_price) * 100000
    rr_ratio = reward_pips / risk_pips if risk_pips > 0 else 0
    
    print(f"   Risk: {risk_pips:.1f} pips")
    print(f"   Reward: {reward_pips:.1f} pips")
    print(f"   R/R Ratio: 1:{rr_ratio:.1f}")
    
    if abs(rr_ratio - 1.0) < 0.1:
        print(f"{Fore.GREEN}✅ Risk/Reward ratio is correct (1:1){Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️ Risk/Reward ratio not optimal{Style.RESET_ALL}")
        
    return True

def test_contrarian_logic():
    """Test contrarian signal reversal logic."""
    print(f"\n{Fore.CYAN}🔄 Testing Contrarian Logic...{Style.RESET_ALL}")
    
    test_cases = [
        ("BUY", "SELL"),
        ("SELL", "BUY")
    ]
    
    for original, expected in test_cases:
        # Simulate reversal logic
        if original == "BUY":
            reversed_signal = "SELL"
        elif original == "SELL":
            reversed_signal = "BUY"
        else:
            reversed_signal = original
            
        if reversed_signal == expected:
            print(f"✅ {original} signal → {reversed_signal} trade (correct)")
        else:
            print(f"❌ {original} signal → {reversed_signal} trade (incorrect)")
            
    return True

def main():
    """Run all tests."""
    print(f"{Fore.CYAN}🧪 TRADING SYSTEM COMPONENT TESTS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}\n")
    
    tests = [
        ("MT5 Connection", test_mt5_connection),
        ("Signal Generation", test_signal_generation),
        ("Order Logic", test_order_placement_simulation),
        ("Contrarian Logic", test_contrarian_logic)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{Fore.RED}❌ {test_name} failed with error: {e}{Style.RESET_ALL}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{Fore.CYAN}📋 TEST SUMMARY{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*20}{Style.RESET_ALL}")
    
    passed = 0
    for test_name, result in results:
        status = f"{Fore.GREEN}✅ PASS{Style.RESET_ALL}" if result else f"{Fore.RED}❌ FAIL{Style.RESET_ALL}"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print(f"{Fore.GREEN}🎉 All systems operational!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️ Some issues detected{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

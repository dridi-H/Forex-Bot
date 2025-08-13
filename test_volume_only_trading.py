#!/usr/bin/env python3
"""
Test Volume-Only Trading System

Test the new volume-based trading approach that only trades on high volume signals.
NO SIGNAL REVERSAL - direct execution based on volume patterns.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.signal_generator import SignalGenerator
from src.volume_analyzer import VolumeAnalyzer
from src.mt5_connector import MT5Connector
from src.config import Config
from colorama import init, Fore, Style
import MetaTrader5 as mt5

# Initialize colorama
init(autoreset=True)

def test_volume_only_signals():
    """Test volume-only signal generation and filtering."""
    print(f"{Fore.CYAN}🎯 TESTING VOLUME-ONLY TRADING SYSTEM{Style.RESET_ALL}")
    print("💡 Strategy: Only trade when volume score ≥ 8.0/10")
    print("🔄 NO SIGNAL REVERSAL - Use signals directly!")
    
    # Connect to MT5
    if not mt5.initialize():
        print(f"{Fore.RED}❌ Failed to initialize MT5{Style.RESET_ALL}")
        return False
    
    # Initialize components
    mt5_connector = MT5Connector()
    if not mt5_connector.connect():
        print(f"{Fore.RED}❌ Failed to connect to MT5{Style.RESET_ALL}")
        return False
    
    config = Config()
    signal_generator = SignalGenerator(mt5_connector, config)
    volume_analyzer = VolumeAnalyzer(mt5_connector)
    
    # Test symbols with 'm' suffix for your broker
    test_symbols = ['EURUSDm', 'GBPUSDm', 'USDJPYm', 'AUDUSDm']
    
    high_volume_signals = []
    
    for symbol in test_symbols:
        print(f"\n{Fore.BLUE}📊 Analyzing {symbol}...{Style.RESET_ALL}")
        
        # Generate signal using day trading mode
        signal = signal_generator.generate_live_day_trading_signal(symbol)
        
        if signal:
            original_signal = signal['signal']
            signal_strength = signal['strength']
            
            # Get volume analysis
            volume_analysis = volume_analyzer.get_volume_contrarian_signals(symbol, ['M5', 'M15', 'H1'])
            
            if volume_analysis and 'combined_analysis' in volume_analysis:
                volume_score = volume_analysis['combined_analysis']['score']
                
                print(f"  📈 Original Signal: {Fore.BLUE}{original_signal}{Style.RESET_ALL}")
                print(f"  ⭐ Signal Strength: {signal_strength:.1f}/10")
                print(f"  📊 Volume Score: {Fore.GREEN if volume_score >= 8.0 else Fore.YELLOW}{volume_score:.1f}/10{Style.RESET_ALL}")
                
                # Volume-only filtering
                if volume_score >= 8.0:
                    # HIGH VOLUME - Trade the signal DIRECTLY (no reversal)
                    final_action = original_signal
                    print(f"  🚀 {Fore.GREEN}HIGH VOLUME CONFIRMED{Style.RESET_ALL}")
                    print(f"  🎯 Final Action: {Fore.GREEN if final_action == 'BUY' else Fore.RED}{final_action}{Style.RESET_ALL} (DIRECT)")
                    
                    # Add volume analysis to signal data
                    signal['volume_analysis'] = volume_analysis
                    signal['volume_score'] = volume_score
                    signal['final_action'] = final_action
                    signal['trade_type'] = 'VOLUME_DIRECT'
                    
                    high_volume_signals.append({
                        'symbol': symbol,
                        'signal': signal,
                        'volume_score': volume_score
                    })
                    
                    # Show volume patterns
                    if 'timeframe_analysis' in volume_analysis:
                        patterns = []
                        for tf, data in volume_analysis['timeframe_analysis'].items():
                            if data.get('price_volume_divergence', {}).get('detected', False):
                                div_type = data['price_volume_divergence']['type']
                                patterns.append(f"{tf} {div_type}")
                            if data.get('exhaustion_signal', {}).get('detected', False):
                                exh_type = data['exhaustion_signal']['type']
                                patterns.append(f"{tf} {exh_type}")
                        
                        if patterns:
                            print(f"  📋 Volume Patterns: {', '.join(patterns)}")
                    
                else:
                    # LOW/MEDIUM VOLUME - Skip trade
                    print(f"  ⏭️ {Fore.YELLOW}VOLUME TOO LOW - SKIPPING TRADE{Style.RESET_ALL}")
                    print("  💡 Need volume score ≥ 8.0 for execution")
            else:
                print("  ❌ No volume analysis available")
        else:
            print("  ❌ No qualifying signal generated")
    
    # Summary
    print(f"\n{Fore.GREEN}🎯 VOLUME-ONLY TRADING SUMMARY{Style.RESET_ALL}")
    print(f"📊 High Volume Signals (≥8.0): {len(high_volume_signals)}")
    
    if high_volume_signals:
        print(f"\n{Fore.CYAN}✅ READY TO EXECUTE:{Style.RESET_ALL}")
        for i, trade in enumerate(high_volume_signals, 1):
            symbol = trade['symbol']
            signal = trade['signal']
            volume_score = trade['volume_score']
            
            print(f"  {i}. {symbol}: {signal['final_action']} (Volume: {volume_score:.1f}/10)")
            print(f"     Signal: {signal['strength']:.1f}/10 | Type: {signal['trade_type']}")
    else:
        print("  💡 No high-volume signals detected - waiting for better setups")
    
    print(f"\n{Fore.YELLOW}📋 STRATEGY SUMMARY:{Style.RESET_ALL}")
    print("  🎯 Volume Threshold: ≥ 8.0/10 (HIGH CONFIDENCE ONLY)")
    print("  🔄 Signal Processing: DIRECT execution (NO REVERSAL)")
    print("  📈 Pattern Detection: Divergences, exhaustion, accumulation")
    print("  💰 Risk Management: Volume-enhanced TP/SL levels")
    
    mt5_connector.disconnect()
    print(f"\n{Fore.GREEN}✅ Volume-Only Trading Test Complete!{Style.RESET_ALL}")
    return True

if __name__ == "__main__":
    test_volume_only_signals()

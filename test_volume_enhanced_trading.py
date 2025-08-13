#!/usr/bin/env python3
"""
Volume-Enhanced Contrarian Trading Test

Tests the new volume analysis integration with the contrarian trading system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from colorama import Fore, Style, init
from src.config import TradingConfig
from src.mt5_connector import MT5Connector
from src.signal_generator import SignalGenerator
from src.volume_analyzer import VolumeAnalyzer

# Initialize colorama
init()


def test_volume_enhanced_signals():
    """Test volume-enhanced signal generation."""
    print(f"\n{Fore.CYAN}🔊 VOLUME-ENHANCED CONTRARIAN TRADING TEST{Style.RESET_ALL}")
    print("=" * 60)
    
    # Initialize components
    config = TradingConfig()
    mt5 = MT5Connector()
    
    if not mt5.connect():
        print(f"❌ Could not connect to MT5")
        return False
    
    # Test volume analyzer independently
    print(f"\n{Fore.YELLOW}📊 Testing Volume Analyzer...{Style.RESET_ALL}")
    volume_analyzer = VolumeAnalyzer(mt5)
    
    # Test symbols with 'm' suffix for MT5 broker
    test_symbols = ['EURUSDm', 'GBPUSDm', 'USDJPYm']
    
    for symbol in test_symbols:
        print(f"\n{Fore.BLUE}🔍 Volume Analysis for {symbol}:{Style.RESET_ALL}")
        
        # Get volume analysis for single timeframe
        volume_profile = volume_analyzer.analyze_volume_profile(symbol, "M15", 50)
        if volume_profile:
            print(f"  📈 Current Volume: {volume_profile['current_volume']:,.0f}")
            print(f"  📊 Volume SMA(20): {volume_profile['volume_sma_20']:,.0f}")
            print(f"  📊 Volume Ratio: {volume_profile['volume_ratio_20']:.2f}x")
            print(f"  🔥 Volume Spike: {'✅ YES' if volume_profile['volume_spike'] else '❌ NO'}")
            print(f"  💧 Volume Dry-up: {'✅ YES' if volume_profile['volume_dry_up'] else '❌ NO'}")
            print(f"  🎯 Contrarian Score: {volume_profile['contrarian_score']:.1f}/10")
            
            # Check for divergences
            divergence = volume_profile['price_volume_divergence']
            if divergence['detected']:
                print(f"  🔄 Divergence: {divergence['type']} (Strength: {divergence['strength']:.1f})")
            
            # Check for exhaustion
            exhaustion = volume_profile['exhaustion_signal']
            if exhaustion['detected']:
                print(f"  💥 Exhaustion: {exhaustion['type']} (Strength: {exhaustion['strength']:.1f})")
        
        # Get multi-timeframe volume signals
        multi_tf_volume = volume_analyzer.get_volume_contrarian_signals(symbol)
        if multi_tf_volume and 'combined_analysis' in multi_tf_volume:
            combined = multi_tf_volume['combined_analysis']
            print(f"  🎯 Combined Volume Score: {combined['score']:.1f}/10")
            print(f"  🔥 Volume Spikes: {combined['volume_spikes_count']}")
            print(f"  🔄 Divergences: {combined['divergences_count']}")
            print(f"  💥 Exhaustions: {combined['exhaustions_count']}")
            
            recommendation = combined['recommendation']
            print(f"  💡 Recommendation: {recommendation['action']} ({recommendation['confidence']} confidence)")
            print(f"     {recommendation['description']}")
    
    # Test enhanced signal generation
    print(f"\n{Fore.YELLOW}🤖 Testing Volume-Enhanced Signal Generation...{Style.RESET_ALL}")
    signal_generator = SignalGenerator(mt5, config)
    
    for symbol in test_symbols:
        print(f"\n{Fore.GREEN}🎯 Enhanced Signal Analysis for {symbol}:{Style.RESET_ALL}")
        
        # Generate signal with volume enhancement
        signal = signal_generator.generate_live_day_trading_signal(symbol)
        
        if signal:
            print(f"  📊 Signal: {signal['signal']}")
            print(f"  ⭐ Base Strength: {signal['strength']:.1f}/10")
            
            if 'volume_score' in signal:
                print(f"  🔊 Volume Score: {signal['volume_score']:.1f}/10")
                print(f"  ⬆️ Volume Boost: {signal['volume_boost']:+.1f}")
                
                # Show volume-specific confluences
                volume_confluences = [c for c in signal['confluences'] if 'Volume' in c or 'Exhaustion' in c or 'Divergence' in c]
                if volume_confluences:
                    print(f"  🎯 Volume Confluences:")
                    for confluence in volume_confluences:
                        print(f"     • {confluence}")
                
                # Show volume recommendation
                if 'volume_recommendation' in signal:
                    rec = signal['volume_recommendation']
                    print(f"  💡 Volume Recommendation: {rec.get('action', 'N/A')}")
                    print(f"     {rec.get('description', 'No description')}")
            
            print(f"  🔗 Total Confluences: {len(signal['confluences'])}")
            
            # Simulate contrarian reversal
            contrarian_action = "SELL" if signal['signal'] == "BUY" else "BUY"
            print(f"  🔄 Contrarian Trade: {signal['signal']} signal → Execute {contrarian_action}")
            
        else:
            print(f"  ❌ No qualifying signal generated")
    
    # Volume pattern detection examples
    print(f"\n{Fore.YELLOW}🔍 Volume Pattern Detection Examples:{Style.RESET_ALL}")
    print(f"  💥 Exhaustion Patterns: High volume on extreme moves → Reversal likely")
    print(f"  🔄 Volume Divergence: Price up + Volume down → Bearish divergence")
    print(f"  📈 Volume Confirmation: Volume spike + Price extreme → Strong reversal signal")
    print(f"  💧 Volume Dry-up: Low volume + Price consolidation → Accumulation phase")
    
    mt5.disconnect()
    print(f"\n{Fore.GREEN}✅ Volume-Enhanced Contrarian Trading Test Complete!{Style.RESET_ALL}")
    return True


def show_volume_benefits():
    """Show the benefits of adding volume analysis."""
    print(f"\n{Fore.CYAN}🚀 VOLUME ANALYSIS BENEFITS FOR YOUR CONTRARIAN SYSTEM{Style.RESET_ALL}")
    print("=" * 70)
    
    benefits = [
        "🎯 **REVERSAL CONFIRMATION**: Volume spikes often mark exhaustion points",
        "🔄 **DIVERGENCE DETECTION**: Price-volume divergence signals trend weakness", 
        "💥 **EXHAUSTION SIGNALS**: Climax volume patterns indicate reversal zones",
        "📊 **SIGNAL FILTERING**: Poor volume patterns filter out weak signals",
        "⭐ **STRENGTH ENHANCEMENT**: Volume confirmation boosts signal strength",
        "🔍 **FALSE BREAKOUT DETECTION**: Low volume breakouts are often false",
        "📈 **ACCUMULATION PHASES**: Volume dry-up often precedes major moves",
        "🎛️ **MULTI-TIMEFRAME CONFIRMATION**: Volume alignment across timeframes"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    print(f"\n{Fore.YELLOW}📋 IMPLEMENTATION FEATURES:{Style.RESET_ALL}")
    features = [
        "✅ Multi-timeframe volume analysis (M5, M15, H1)",
        "✅ Price-volume divergence detection",
        "✅ Volume exhaustion pattern recognition", 
        "✅ Accumulation/Distribution indicator",
        "✅ Volume trend analysis",
        "✅ Contrarian-specific volume scoring",
        "✅ Signal strength enhancement",
        "✅ Volume-based signal filtering"
    ]
    
    for feature in features:
        print(f"  {feature}")


if __name__ == "__main__":
    show_volume_benefits()
    test_volume_enhanced_signals()

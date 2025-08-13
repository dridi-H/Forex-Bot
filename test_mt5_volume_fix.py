#!/usr/bin/env python3
"""
MT5 Volume Data Test

Tests how to properly extract volume data from MetaTrader 5.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import MetaTrader5 as mt5
import numpy as np
from colorama import Fore, Style, init
from src.mt5_connector import MT5Connector

# Initialize colorama
init()


def test_mt5_volume_data():
    """Test MT5 volume data extraction."""
    print(f"\n{Fore.CYAN}🔬 MT5 VOLUME DATA ANALYSIS{Style.RESET_ALL}")
    print("=" * 50)
    
    # Connect to MT5
    connector = MT5Connector()
    if not connector.connect():
        print(f"❌ Could not connect to MT5")
        return False
    
    # Test symbol with 'm' suffix
    symbol = "EURUSDm"
    timeframe = "M15"
    periods = 20
    
    print(f"\n{Fore.YELLOW}📊 Testing {symbol} on {timeframe} for {periods} periods{Style.RESET_ALL}")
    
    # Get raw MT5 data
    print(f"\n{Fore.BLUE}🔍 Raw MT5 Data Structure:{Style.RESET_ALL}")
    rates = connector.get_rates(symbol, timeframe, periods)
    
    if rates is not None and len(rates) > 0:
        print(f"✅ Got {len(rates)} bars")
        print(f"📊 Data type: {type(rates)}")
        print(f"📊 Single bar type: {type(rates[0])}")
        print(f"📊 Available fields: {rates.dtype.names if hasattr(rates, 'dtype') else 'No dtype'}")
        
        # Show first bar details
        if len(rates) > 0:
            first_bar = rates[0]
            print(f"\n{Fore.GREEN}📈 First Bar Analysis:{Style.RESET_ALL}")
            print(f"  📅 Time: {first_bar['time'] if 'time' in first_bar.dtype.names else 'N/A'}")
            print(f"  💰 Open: {first_bar['open'] if 'open' in first_bar.dtype.names else 'N/A'}")
            print(f"  📈 High: {first_bar['high'] if 'high' in first_bar.dtype.names else 'N/A'}")
            print(f"  📉 Low: {first_bar['low'] if 'low' in first_bar.dtype.names else 'N/A'}")
            print(f"  💰 Close: {first_bar['close'] if 'close' in first_bar.dtype.names else 'N/A'}")
            
            # Volume analysis
            if 'tick_volume' in first_bar.dtype.names:
                print(f"  🔊 Tick Volume: {first_bar['tick_volume']}")
            if 'real_volume' in first_bar.dtype.names:
                print(f"  🔊 Real Volume: {first_bar['real_volume']}")
            if 'spread' in first_bar.dtype.names:
                print(f"  📏 Spread: {first_bar['spread']}")
        
        # Test volume extraction methods
        print(f"\n{Fore.YELLOW}🔊 Volume Extraction Tests:{Style.RESET_ALL}")
        
        # Method 1: Direct field access
        try:
            volumes_method1 = rates['tick_volume']
            print(f"✅ Method 1 (Direct access): {len(volumes_method1)} volumes")
            print(f"   📊 Type: {type(volumes_method1)}")
            print(f"   📊 Sample: {volumes_method1[:5]}")
            print(f"   📊 Latest: {volumes_method1[-1]}")
        except Exception as e:
            print(f"❌ Method 1 failed: {e}")
        
        # Method 2: List comprehension (current problematic method)
        try:
            volumes_method2 = [rate['tick_volume'] for rate in rates]
            print(f"✅ Method 2 (List comprehension): {len(volumes_method2)} volumes")
            print(f"   📊 Type: {type(volumes_method2)}")
            print(f"   📊 Sample: {volumes_method2[:5]}")
            print(f"   📊 Latest: {volumes_method2[-1]}")
        except Exception as e:
            print(f"❌ Method 2 failed: {e}")
        
        # Method 3: NumPy array conversion
        try:
            volumes_method3 = np.array(rates['tick_volume'])
            print(f"✅ Method 3 (NumPy conversion): {len(volumes_method3)} volumes")
            print(f"   📊 Type: {type(volumes_method3)}")
            print(f"   📊 Sample: {volumes_method3[:5]}")
            print(f"   📊 Latest: {volumes_method3[-1]}")
            
            # Test calculations
            avg_volume = np.mean(volumes_method3)
            current_volume = volumes_method3[-1]
            volume_ratio = current_volume / avg_volume
            
            print(f"   📊 Average Volume: {avg_volume:.0f}")
            print(f"   📊 Current Volume: {current_volume}")
            print(f"   📊 Volume Ratio: {volume_ratio:.2f}x")
            
            # Test volume spike detection
            volume_spike = current_volume > (avg_volume * 1.5)
            print(f"   🔥 Volume Spike: {'✅ YES' if volume_spike else '❌ NO'}")
            
        except Exception as e:
            print(f"❌ Method 3 failed: {e}")
    
    else:
        print(f"❌ No data received")
    
    connector.disconnect()
    return True


def create_fixed_volume_analyzer():
    """Create a fixed version of the volume analyzer."""
    print(f"\n{Fore.CYAN}🔧 CREATING FIXED VOLUME ANALYZER{Style.RESET_ALL}")
    print("=" * 50)
    
    fixed_code = '''
    def analyze_volume_profile_fixed(self, symbol, timeframe="M15", periods=50):
        """
        FIXED: Analyze volume profile for contrarian opportunities.
        
        Args:
            symbol (str): Currency pair
            timeframe (str): Timeframe for analysis
            periods (int): Number of periods to analyze
            
        Returns:
            dict: Volume analysis results
        """
        try:
            # Get OHLCV data
            rates = self.mt5.get_rates(symbol, timeframe, periods)
            if rates is None or len(rates) < 20:
                return None
                
            # FIXED: Extract volume data properly from MT5 structured array
            volumes = rates['tick_volume']  # Direct field access (no list comprehension)
            prices = rates['close']         # Direct field access
            highs = rates['high']          # Direct field access
            lows = rates['low']            # Direct field access
            
            # Convert to float for calculations
            volumes = np.array(volumes, dtype=float)
            prices = np.array(prices, dtype=float)
            highs = np.array(highs, dtype=float)
            lows = np.array(lows, dtype=float)
            
            # Calculate volume metrics
            volume_sma_20 = float(np.mean(volumes[-20:]))
            volume_sma_50 = float(np.mean(volumes) if len(volumes) >= 50 else np.mean(volumes))
            current_volume = float(volumes[-1])
            
            # Volume analysis
            analysis = {
                'current_volume': current_volume,
                'volume_sma_20': volume_sma_20,
                'volume_sma_50': volume_sma_50,
                'volume_ratio_20': current_volume / volume_sma_20 if volume_sma_20 > 0 else 1,
                'volume_ratio_50': current_volume / volume_sma_50 if volume_sma_50 > 0 else 1,
                'volume_spike': bool(current_volume > (volume_sma_20 * 1.5)),
                'volume_dry_up': bool(current_volume < (volume_sma_20 * 0.7)),
                'contrarian_score': 0
            }
            
            # Calculate contrarian volume score
            analysis['contrarian_score'] = self._calculate_contrarian_volume_score_fixed(analysis)
            
            return analysis
            
        except Exception as e:
            print(f"❌ Volume analysis error for {symbol}: {e}")
            return None
    '''
    
    print("🔧 Fixed volume extraction method:")
    print("   ✅ Use direct field access: rates['tick_volume']")
    print("   ✅ Avoid list comprehension with structured arrays")
    print("   ✅ Convert to numpy arrays with explicit dtype")
    print("   ✅ Handle MT5 data structure properly")
    
    return fixed_code


if __name__ == "__main__":
    print(f"{Fore.GREEN}🚀 MT5 Volume Data Analysis Tool{Style.RESET_ALL}")
    test_mt5_volume_data()
    create_fixed_volume_analyzer()

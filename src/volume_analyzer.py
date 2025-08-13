#!/usr/bin/env python3
"""
Volume Analyzer for Contrarian Trading System

Analyzes tick volume patterns to enhance contrarian signal detection.
In Forex, we use tick volume (number of price changes) as a proxy for activity.
"""

import numpy as np
from datetime import datetime
from colorama import Fore, Style


class VolumeAnalyzer:
    """
    Volume Analysis for Forex Contrarian Trading
    
    Analyzes tick volume patterns to identify:
    - Volume exhaustion signals
    - Reversal confirmation
    - False breakout detection
    - Volume-price divergences
    """
    
    def __init__(self, mt5_connector):
        """Initialize volume analyzer."""
        self.mt5 = mt5_connector
        
    def analyze_volume_profile(self, symbol, timeframe="M15", periods=50):
        """
        Analyze volume profile for contrarian opportunities.
        
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
            # MT5 returns structured numpy array with fields: ('time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume')
            volumes = np.array(rates['tick_volume'], dtype=float)  # Direct field access
            prices = np.array(rates['close'], dtype=float)         # Direct field access  
            highs = np.array(rates['high'], dtype=float)          # Direct field access
            lows = np.array(rates['low'], dtype=float)            # Direct field access
            
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
                'price_volume_divergence': self._detect_price_volume_divergence(prices[-10:], volumes[-10:]),
                'exhaustion_signal': self._detect_exhaustion_volume(prices, volumes, highs, lows),
                'accumulation_distribution': self._calculate_accumulation_distribution(rates[-20:]),
                'volume_trend': self._analyze_volume_trend(volumes[-10:]),
                'contrarian_score': 0  # Will be calculated
            }
            
            # Calculate contrarian volume score
            analysis['contrarian_score'] = self._calculate_contrarian_volume_score(analysis)
            
            return analysis
            
        except Exception as e:
            print(f"❌ Volume analysis error for {symbol}: {e}")
            return None
    
    def _detect_price_volume_divergence(self, prices, volumes):
        """
        Detect price-volume divergence (contrarian signal).
        
        Returns:
            dict: Divergence analysis
        """
        if len(prices) < 5 or len(volumes) < 5:
            return {'detected': False, 'type': None, 'strength': 0}
        
        # Calculate price momentum
        price_momentum = (prices[-1] - prices[0]) / prices[0]
        
        # Calculate volume momentum  
        volume_momentum = (np.mean(volumes[-3:]) - np.mean(volumes[:3])) / np.mean(volumes[:3])
        
        # Detect divergence
        if price_momentum > 0.001 and volume_momentum < -0.2:  # Price up, volume down
            return {
                'detected': True,
                'type': 'bearish_divergence',  # Contrarian SELL opportunity
                'strength': abs(volume_momentum) * 100,
                'description': 'Price rising on declining volume - potential reversal'
            }
        elif price_momentum < -0.001 and volume_momentum < -0.2:  # Price down, volume down
            return {
                'detected': True,
                'type': 'bullish_divergence',  # Contrarian BUY opportunity  
                'strength': abs(volume_momentum) * 100,
                'description': 'Price falling on declining volume - potential reversal'
            }
        
        return {'detected': False, 'type': None, 'strength': 0}
    
    def _detect_exhaustion_volume(self, prices, volumes, highs, lows):
        """
        Detect volume exhaustion patterns (strong contrarian signals).
        
        Returns:
            dict: Exhaustion analysis
        """
        if len(volumes) < 10:
            return {'detected': False, 'type': None, 'strength': 0}
        
        # Get recent data
        recent_volumes = volumes[-5:]
        recent_prices = prices[-5:]
        recent_highs = highs[-5:]
        recent_lows = lows[-5:]
        
        # Check for climax volume patterns
        max_volume_idx = np.argmax(recent_volumes)
        max_volume = float(recent_volumes[max_volume_idx])
        avg_volume = float(np.mean(volumes[-20:] if len(volumes) >= 20 else volumes))
        
        # Volume spike conditions
        is_volume_spike = bool(max_volume > (avg_volume * 2.0))
        
        if is_volume_spike and max_volume_idx >= 3:  # Volume spike not on latest bar
            # Check if price action suggests exhaustion
            price_range = float(recent_highs[max_volume_idx] - recent_lows[max_volume_idx])
            avg_range = float(np.mean(recent_highs - recent_lows))
            
            if price_range > avg_range * 1.5:  # Wide range bar
                # Determine exhaustion type
                if float(recent_prices[max_volume_idx]) > float(recent_prices[0]):  # Upward move
                    return {
                        'detected': True,
                        'type': 'buying_exhaustion',  # Contrarian SELL signal
                        'strength': (max_volume / avg_volume) * 10,
                        'description': f'High volume exhaustion on upward move at bar {max_volume_idx}'
                    }
                else:  # Downward move
                    return {
                        'detected': True,
                        'type': 'selling_exhaustion',  # Contrarian BUY signal
                        'strength': (max_volume / avg_volume) * 10,
                        'description': f'High volume exhaustion on downward move at bar {max_volume_idx}'
                    }
        
        return {'detected': False, 'type': None, 'strength': 0}
    
    def _calculate_accumulation_distribution(self, rates):
        """
        Calculate Accumulation/Distribution indicator.
        
        Returns:
            dict: A/D analysis
        """
        if len(rates) < 10:
            return {'value': 0, 'trend': 'neutral', 'signal': None}
        
        ad_values = []
        
        for rate in rates:
            # Money Flow Multiplier
            clv = ((rate['close'] - rate['low']) - (rate['high'] - rate['close'])) / (rate['high'] - rate['low'])
            if rate['high'] == rate['low']:  # Avoid division by zero
                clv = 0
            
            # Money Flow Volume
            mfv = clv * rate['tick_volume']
            ad_values.append(mfv)
        
        # Calculate trend
        ad_sma_short = np.mean(ad_values[-5:])
        ad_sma_long = np.mean(ad_values[-10:] if len(ad_values) >= 10 else ad_values)
        
        if ad_sma_short > ad_sma_long * 1.1:
            trend = 'accumulation'  # Potential bearish divergence for contrarian
            signal = 'contrarian_sell_bias'
        elif ad_sma_short < ad_sma_long * 0.9:
            trend = 'distribution'  # Potential bullish divergence for contrarian
            signal = 'contrarian_buy_bias'
        else:
            trend = 'neutral'
            signal = None
        
        return {
            'value': ad_sma_short,
            'trend': trend,
            'signal': signal,
            'ratio': ad_sma_short / ad_sma_long if ad_sma_long != 0 else 1
        }
    
    def _analyze_volume_trend(self, volumes):
        """
        Analyze volume trend direction.
        
        Returns:
            dict: Volume trend analysis
        """
        if len(volumes) < 5:
            return {'trend': 'insufficient_data', 'strength': 0}
        
        # Linear regression on volume
        x = np.arange(len(volumes))
        slope = np.polyfit(x, volumes, 1)[0]
        avg_volume = np.mean(volumes)
        
        # Normalize slope
        trend_strength = abs(slope) / avg_volume if avg_volume > 0 else 0
        
        if slope > avg_volume * 0.1:
            return {'trend': 'increasing', 'strength': trend_strength, 'signal': 'volume_expansion'}
        elif slope < -avg_volume * 0.1:
            return {'trend': 'decreasing', 'strength': trend_strength, 'signal': 'volume_contraction'}
        else:
            return {'trend': 'stable', 'strength': trend_strength, 'signal': 'volume_steady'}
    
    def _calculate_contrarian_volume_score(self, analysis):
        """
        Calculate overall contrarian volume score (0-10).
        
        Returns:
            float: Contrarian volume score
        """
        score = 5.0  # Base score
        
        # Volume spike bonus (potential exhaustion)
        if analysis['volume_spike']:
            score += 2.0
        
        # Volume dry-up bonus (potential accumulation before reversal)
        if analysis['volume_dry_up']:
            score += 1.0
        
        # Price-volume divergence bonus
        if analysis['price_volume_divergence']['detected']:
            score += analysis['price_volume_divergence']['strength'] / 10
        
        # Exhaustion pattern bonus
        if analysis['exhaustion_signal']['detected']:
            score += min(3.0, analysis['exhaustion_signal']['strength'] / 10)
        
        # Accumulation/Distribution signal
        if analysis['accumulation_distribution']['signal']:
            score += 1.0
        
        # Volume trend consideration
        volume_trend = analysis['volume_trend']
        if volume_trend['trend'] == 'decreasing' and volume_trend['strength'] > 0.2:
            score += 1.0  # Decreasing volume can signal reversal
        
        return min(10.0, max(0.0, score))
    
    def get_volume_contrarian_signals(self, symbol, timeframes=['M5', 'M15', 'H1']):
        """
        Get comprehensive volume-based contrarian signals.
        
        Args:
            symbol (str): Currency pair
            timeframes (list): Timeframes to analyze
            
        Returns:
            dict: Multi-timeframe volume analysis
        """
        results = {}
        
        for tf in timeframes:
            analysis = self.analyze_volume_profile(symbol, tf)
            if analysis:
                results[tf] = analysis
        
        # Calculate combined score
        if results:
            combined_score = np.mean([results[tf]['contrarian_score'] for tf in results.keys()])
            
            # Multi-timeframe confirmation bonus
            volume_spikes = sum(1 for tf in results.keys() if results[tf]['volume_spike'])
            divergences = sum(1 for tf in results.keys() if results[tf]['price_volume_divergence']['detected'])
            exhaustions = sum(1 for tf in results.keys() if results[tf]['exhaustion_signal']['detected'])
            
            if volume_spikes >= 2:
                combined_score += 1.0
            if divergences >= 2:
                combined_score += 1.5
            if exhaustions >= 1:
                combined_score += 2.0
            
            results['combined_analysis'] = {
                'score': min(10.0, combined_score),
                'volume_spikes_count': volume_spikes,
                'divergences_count': divergences,
                'exhaustions_count': exhaustions,
                'recommendation': self._get_volume_recommendation(combined_score, results)
            }
        
        return results
    
    def _get_volume_recommendation(self, score, results):
        """Get volume-based trading recommendation."""
        if score >= 8.0:
            return {
                'action': 'strong_contrarian_signal',
                'confidence': 'high',
                'description': 'Strong volume patterns support contrarian trade'
            }
        elif score >= 6.5:
            return {
                'action': 'moderate_contrarian_signal', 
                'confidence': 'medium',
                'description': 'Moderate volume support for contrarian approach'
            }
        elif score >= 5.0:
            return {
                'action': 'neutral',
                'confidence': 'low',
                'description': 'Neutral volume patterns - wait for better setup'
            }
        else:
            return {
                'action': 'avoid',
                'confidence': 'low', 
                'description': 'Volume patterns do not support contrarian trade'
            }


def main():
    """Test volume analyzer."""
    print(f"{Fore.CYAN}🔊 Volume Analyzer Test{Style.RESET_ALL}")
    print("Volume analysis module ready for integration!")


if __name__ == "__main__":
    main()

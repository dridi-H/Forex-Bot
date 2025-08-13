#!/usr/bin/env python3
"""
Signal Generator for Contrarian Trading System

Generates ultra-strict trading signals with multi-timeframe analysis.
Signals are designed to be reversed for contrarian trading.
"""

import numpy as np
from datetime import datetime, timedelta
from colorama import Fore, Style


class SignalGenerator:
    """
    Advanced Signal Generator with Multi-Timeframe Analysis
    
    Generates high-quality signals for contrarian reversal trading.
    """
    
    def __init__(self, mt5_connector, config):
        """Initialize the signal generator."""
        self.mt5 = mt5_connector
        self.config = config
        # Initialize volume analyzer for enhanced signals
        try:
            from volume_analyzer import VolumeAnalyzer
            self.volume_analyzer = VolumeAnalyzer(mt5_connector)
            self.volume_enabled = True
            print(f"{Fore.GREEN}✅ Volume analysis enabled{Style.RESET_ALL}")
        except ImportError:
            self.volume_analyzer = None
            self.volume_enabled = False
            print(f"{Fore.YELLOW}⚠️ Volume analyzer not available{Style.RESET_ALL}")
        
    def generate_live_day_trading_signal(self, symbol):
        """
        Generate optimized day trading signal for a symbol.
        
        OPTIMIZED FOR DAY TRADING:
        - 4H (48 bars) - Market structure & trend bias
        - 1H (100 bars) - Entry confirmation  
        - 15M (96 bars) - Precise timing (last 24 hours)
        - 5M (288 bars) - Execution precision (last 24 hours)
        
        Args:
            symbol (str): Trading symbol
            
        Returns:
            dict: Signal data with type, strength, and confluences
        """
        try:
            print(f"🔍 Getting optimized day trading data for {symbol}...")
            
            # Get optimized multi-timeframe data for day trading
            m5_data = self.mt5.get_rates(symbol, "M5", 288)   # 5min: 288 bars = 24 hours
            m15_data = self.mt5.get_rates(symbol, "M15", 96)  # 15min: 96 bars = 24 hours
            h1_data = self.mt5.get_rates(symbol, "H1", 100)   # 1H: 100 bars = ~4 days
            h4_data = self.mt5.get_rates(symbol, "H4", 48)    # 4H: 48 bars = 8 days
            
            print(f"📊 Day trading data received: 5M={len(m5_data) if m5_data is not None else 'None'}, "
                  f"15M={len(m15_data) if m15_data is not None else 'None'}, "
                  f"1H={len(h1_data) if h1_data is not None else 'None'}, "
                  f"4H={len(h4_data) if h4_data is not None else 'None'}")
            
            if not all([m5_data is not None, m15_data is not None, h1_data is not None, h4_data is not None]):
                print(f"❌ Missing day trading data for {symbol}")
                return None
                
            # Analyze each timeframe for day trading
            print(f"📈 Analyzing day trading timeframes...")
            m5_analysis = self._analyze_timeframe(m5_data, "M5")
            m15_analysis = self._analyze_timeframe(m15_data, "M15")
            h1_analysis = self._analyze_timeframe(h1_data, "H1")
            h4_analysis = self._analyze_timeframe(h4_data, "H4")
            
            if not all([m5_analysis, m15_analysis, h1_analysis, h4_analysis]):
                print(f"❌ Day trading analysis failed for {symbol}")
                return None
            
            # Combine analysis with day trading focus
            signal_data = self._combine_day_trading_analysis(symbol, m5_analysis, m15_analysis, h1_analysis, h4_analysis)
            
            # Enhance with volume analysis if available
            if signal_data and self.volume_enabled:
                signal_data = self._enhance_with_volume_analysis(symbol, signal_data)
            
            if signal_data:
                print(f"✅ Day trading signal generated for {symbol}: {signal_data['signal']} {signal_data['strength']:.1f}/10")
                if 'volume_score' in signal_data:
                    print(f"🔊 Volume Score: {signal_data['volume_score']:.1f}/10")
            else:
                print(f"⚠️ No qualifying day trading signal for {symbol}")
            
            return signal_data
            
        except Exception as e:
            print(f"❌ Day trading signal generation error for {symbol}: {e}")
            return None
    
    def _combine_day_trading_analysis(self, symbol, m5, m15, h1, h4):
        """
        Combine multi-timeframe analysis for optimized day trading signals.
        
        TIMEFRAME HIERARCHY:
        - M5: Execution precision and micro-momentum
        - M15: Entry timing and short-term momentum  
        - H1: Trend confirmation and structure
        - H4: Market bias and major levels
        """
        if not all([m5, m15, h1, h4]):
            return None
            
        confluences = []
        bullish_signals = 0
        bearish_signals = 0
        
        # === M5 PRECISION ANALYSIS (Execution Level) ===
        if m5['rsi'] > 75:  # Extreme overbought on M5
            bearish_signals += 3
            confluences.append("M5 RSI Extreme Overbought (75+)")
            
        if m5['rsi'] < 25:  # Extreme oversold on M5
            bullish_signals += 3
            confluences.append("M5 RSI Extreme Oversold (25-)")
            
        # M5 MACD momentum
        if m5['macd'] > m5['macd_signal'] and m5['macd'] > 0:
            bearish_signals += 1  # Strong bullish momentum - contrarian SELL
            confluences.append("M5 MACD Strong Bullish")
            
        if m5['macd'] < m5['macd_signal'] and m5['macd'] < 0:
            bullish_signals += 1  # Strong bearish momentum - contrarian BUY
            confluences.append("M5 MACD Strong Bearish")
            
        # === M15 TIMING ANALYSIS (Entry Level) ===
        if m15['rsi'] > 70:
            bearish_signals += 2
            confluences.append("M15 RSI Overbought (70+)")
            
        if m15['rsi'] < 30:
            bullish_signals += 2
            confluences.append("M15 RSI Oversold (30-)")
            
        # M15 Price position vs EMAs
        if m15['price'] > m15['ema_20'] > m15['ema_50']:
            bearish_signals += 2  # Strong uptrend - contrarian SELL opportunity
            confluences.append("M15 Strong Uptrend")
            
        if m15['price'] < m15['ema_20'] < m15['ema_50']:
            bullish_signals += 2  # Strong downtrend - contrarian BUY opportunity
            confluences.append("M15 Strong Downtrend")
            
        # === H1 CONFIRMATION ANALYSIS ===
        if h1['rsi'] > 65:
            bearish_signals += 1
            confluences.append("H1 RSI High")
            
        if h1['rsi'] < 35:
            bullish_signals += 1
            confluences.append("H1 RSI Low")
            
        # H1 Bollinger Bands (key for contrarian entries)
        if h1['price'] > h1['bb_upper']:
            bearish_signals += 3  # Price above upper band - strong contrarian SELL
            confluences.append("H1 Price Above Bollinger Upper")
            
        if h1['price'] < h1['bb_lower']:
            bullish_signals += 3  # Price below lower band - strong contrarian BUY
            confluences.append("H1 Price Below Bollinger Lower")
            
        # === H4 BIAS ANALYSIS (Market Structure) ===
        if h4['rsi'] > 60:
            bearish_signals += 1
            confluences.append("H4 RSI Overbought Bias")
            
        if h4['rsi'] < 40:
            bullish_signals += 1
            confluences.append("H4 RSI Oversold Bias")
            
        # === MULTI-TIMEFRAME ALIGNMENT ===
        # RSI alignment across timeframes (stronger signal)
        rsi_aligned_bearish = (m5['rsi'] > 70 and m15['rsi'] > 65 and h1['rsi'] > 60)
        rsi_aligned_bullish = (m5['rsi'] < 30 and m15['rsi'] < 35 and h1['rsi'] < 40)
        
        if rsi_aligned_bearish:
            bearish_signals += 2
            confluences.append("Multi-TF RSI Overbought Alignment")
            
        if rsi_aligned_bullish:
            bullish_signals += 2
            confluences.append("Multi-TF RSI Oversold Alignment")
            
        # === SUPPORT/RESISTANCE ANALYSIS ===
        current_price = m5['price']  # Use M5 for precision
        
        # Check proximity to H1 levels (most relevant for day trading)
        if current_price >= h1['resistance'] * 0.9995:  # Very close to resistance
            bearish_signals += 2
            confluences.append("Near H1 Resistance Level")
            
        if current_price <= h1['support'] * 1.0005:  # Very close to support
            bullish_signals += 2
            confluences.append("Near H1 Support Level")
            
        # === DAY TRADING MOMENTUM ANALYSIS ===
        # Check for momentum divergence (contrarian opportunity)
        price_momentum_up = (m15['price'] > m15['ema_20'] and h1['price'] > h1['ema_20'])
        price_momentum_down = (m15['price'] < m15['ema_20'] and h1['price'] < h1['ema_20'])
        
        if price_momentum_up and (m5['rsi'] > 70 or m15['rsi'] > 70):
            bearish_signals += 2
            confluences.append("Momentum Up + RSI Overbought")
            
        if price_momentum_down and (m5['rsi'] < 30 or m15['rsi'] < 30):
            bullish_signals += 2
            confluences.append("Momentum Down + RSI Oversold")
            
        # === SIGNAL DETERMINATION ===
        total_signals = bullish_signals + bearish_signals
        
        if total_signals == 0:
            return None
            
        # Require minimum signal strength for day trading
        min_required_signals = 4  # Reduced from 3 to 4 for better quality
        
        if bullish_signals > bearish_signals and bullish_signals >= min_required_signals:
            signal_type = "BUY"  # Will be reversed to SELL for contrarian
            strength = min(10.0, (bullish_signals / max(total_signals, 1)) * 10)
        elif bearish_signals > bullish_signals and bearish_signals >= min_required_signals:
            signal_type = "SELL"  # Will be reversed to BUY for contrarian
            strength = min(10.0, (bearish_signals / max(total_signals, 1)) * 10)
        else:
            return None
            
        # Apply day trading specific filtering
        strength = self._apply_day_trading_filtering(strength, confluences, m5, m15, h1, h4)
        
        if strength < 6.0:  # Minimum strength for day trading
            return None
            
        return {
            'symbol': symbol,
            'signal': signal_type,
            'strength': round(strength, 1),
            'confluences': confluences,
            'timeframes': {
                'M5': m5,
                'M15': m15,
                'H1': h1,
                'H4': h4
            }
        }
    
    def _apply_day_trading_filtering(self, base_strength, confluences, m5, m15, h1, h4):
        """Apply day trading specific filtering to signal strength."""
        strength = base_strength
        
        # Bonus for multiple confluences (day trading needs more confirmation)
        confluence_count = len(confluences)
        if confluence_count >= 7:
            strength += 1.5
        elif confluence_count >= 5:
            strength += 1.0
        elif confluence_count >= 3:
            strength += 0.5
            
        # M5 precision bonus (critical for day trading)
        if m5['rsi'] > 80 or m5['rsi'] < 20:  # Extreme M5 RSI
            strength += 1.0
        elif m5['rsi'] > 75 or m5['rsi'] < 25:  # Very high/low M5 RSI
            strength += 0.5
            
        # Multi-timeframe RSI alignment bonus
        rsi_spread_m5_m15 = abs(m5['rsi'] - m15['rsi'])
        rsi_spread_m15_h1 = abs(m15['rsi'] - h1['rsi'])
        
        if rsi_spread_m5_m15 < 10 and rsi_spread_m15_h1 < 15:  # Good alignment
            strength += 0.5
            
        # Volatility check (critical for day trading)
        if m5['atr'] < 0.00005:  # Too low volatility
            strength -= 3.0
        elif m5['atr'] < 0.0001:  # Low volatility
            strength -= 1.0
            
        # Bollinger band extreme bonus (great for contrarian)
        bb_position_h1 = 0
        if h1['price'] > h1['bb_upper']:
            bb_position_h1 = (h1['price'] - h1['bb_upper']) / h1['bb_upper']
            strength += min(1.0, bb_position_h1 * 1000)  # Bonus for distance above upper band
        elif h1['price'] < h1['bb_lower']:
            bb_position_h1 = (h1['bb_lower'] - h1['price']) / h1['bb_lower']
            strength += min(1.0, bb_position_h1 * 1000)  # Bonus for distance below lower band
            
        # Penalize signals in neutral zones
        if 40 <= m15['rsi'] <= 60:  # M15 RSI in neutral zone
            strength -= 1.5
            
        if 45 <= h1['rsi'] <= 55:  # H1 RSI in neutral zone
            strength -= 1.0
            
        return max(0, min(10, strength))
            
    def _analyze_timeframe(self, rates, timeframe):
        """Analyze a single timeframe."""
        try:
            if rates is None or len(rates) < 30:  # Reduced from 50 to 30
                print(f"❌ Insufficient data for {timeframe}: {len(rates) if rates is not None else 'None'} bars")
                return None
                
            close = rates['close']
            high = rates['high']
            low = rates['low']
            
            print(f"📊 {timeframe}: Analyzing {len(close)} bars, Current price: {close[-1]:.5f}")
            
            # Technical indicators
            rsi = self._calculate_rsi(close)
            ema_20 = self._calculate_ema(close, 20)
            ema_50 = self._calculate_ema(close, 50)
            macd_line, macd_signal = self._calculate_macd(close)
            bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(close)
            atr = self._calculate_atr(high, low, close)
            
            # Support and resistance
            support, resistance = self._find_support_resistance(high, low, close)
            
            # Current values
            current_price = close[-1]
            current_rsi = rsi[-1] if len(rsi) > 0 else 50
            current_macd = macd_line[-1] if len(macd_line) > 0 else 0
            current_macd_signal = macd_signal[-1] if len(macd_signal) > 0 else 0
            
            print(f"📈 {timeframe}: RSI={current_rsi:.1f}, EMA20={ema_20[-1] if len(ema_20) > 0 else 'N/A':.5f}")
            
            analysis = {
                'timeframe': timeframe,
                'price': current_price,
                'rsi': current_rsi,
                'ema_20': ema_20[-1] if len(ema_20) > 0 else current_price,
                'ema_50': ema_50[-1] if len(ema_50) > 0 else current_price,
                'macd': current_macd,
                'macd_signal': current_macd_signal,
                'bb_upper': bb_upper[-1] if len(bb_upper) > 0 else current_price,
                'bb_lower': bb_lower[-1] if len(bb_lower) > 0 else current_price,
                'support': support,
                'resistance': resistance,
                'atr': atr[-1] if len(atr) > 0 else 0.001
            }
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing {timeframe}: {e}")
            return None
        
    def _combine_analysis(self, symbol, h1, h4, d1):
        """Legacy method - redirects to day trading analysis for compatibility."""
        # For backwards compatibility, convert to day trading format
        # Get additional M5 and M15 data if needed
        try:
            m5_data = self.mt5.get_rates(symbol, "M5", 288)
            m15_data = self.mt5.get_rates(symbol, "M15", 96)
            
            if m5_data is not None and m15_data is not None:
                m5_analysis = self._analyze_timeframe(m5_data, "M5")
                m15_analysis = self._analyze_timeframe(m15_data, "M15")
                
                if m5_analysis and m15_analysis:
                    return self._combine_day_trading_analysis(symbol, m5_analysis, m15_analysis, h1, h4)
        except:
            pass
            
        # Fallback to original analysis if M5/M15 not available
        return self._combine_legacy_analysis(symbol, h1, h4, d1)
    
    def _combine_legacy_analysis(self, symbol, h1, h4, d1):
        """Combine multi-timeframe analysis into final signal."""
        if not all([h1, h4, d1]):
            return None
            
        confluences = []
        bullish_signals = 0
        bearish_signals = 0
        
        # RSI Analysis (for contrarian signals, we look for extremes)
        if h1['rsi'] > 70:  # Overbought - potential contrarian SELL signal
            bearish_signals += 2
            confluences.append("H1 RSI Overbought (70+)")
            
        if h1['rsi'] < 30:  # Oversold - potential contrarian BUY signal
            bullish_signals += 2
            confluences.append("H1 RSI Oversold (30-)")
            
        # H4 RSI confirmation
        if h4['rsi'] > 65:
            bearish_signals += 1
            confluences.append("H4 RSI High")
            
        if h4['rsi'] < 35:
            bullish_signals += 1
            confluences.append("H4 RSI Low")
            
        # Moving Average Analysis
        if h1['price'] > h1['ema_20'] > h1['ema_50']:
            bearish_signals += 1  # Strong uptrend - contrarian SELL opportunity
            confluences.append("H1 Strong Uptrend")
            
        if h1['price'] < h1['ema_20'] < h1['ema_50']:
            bullish_signals += 1  # Strong downtrend - contrarian BUY opportunity
            confluences.append("H1 Strong Downtrend")
            
        # MACD Analysis
        if h1['macd'] > h1['macd_signal'] and h1['macd'] > 0:
            bearish_signals += 1  # Strong bullish momentum - contrarian SELL
            confluences.append("H1 MACD Bullish")
            
        if h1['macd'] < h1['macd_signal'] and h1['macd'] < 0:
            bullish_signals += 1  # Strong bearish momentum - contrarian BUY
            confluences.append("H1 MACD Bearish")
            
        # Bollinger Bands (extremes for contrarian)
        if h1['price'] > h1['bb_upper']:
            bearish_signals += 2  # Price above upper band - contrarian SELL
            confluences.append("Price Above Bollinger Upper Band")
            
        if h1['price'] < h1['bb_lower']:
            bullish_signals += 2  # Price below lower band - contrarian BUY
            confluences.append("Price Below Bollinger Lower Band")
            
        # Support/Resistance Analysis
        current_price = h1['price']
        
        if current_price >= h1['resistance'] * 0.998:  # Near resistance
            bearish_signals += 1
            confluences.append("Near Resistance Level")
            
        if current_price <= h1['support'] * 1.002:  # Near support
            bullish_signals += 1
            confluences.append("Near Support Level")
            
        # Higher timeframe confirmation
        if h4['rsi'] > 60 and d1['rsi'] > 55:
            bearish_signals += 1
            confluences.append("Multi-timeframe Overbought")
            
        if h4['rsi'] < 40 and d1['rsi'] < 45:
            bullish_signals += 1
            confluences.append("Multi-timeframe Oversold")
            
        # Determine signal
        signal_type = None
        total_signals = bullish_signals + bearish_signals
        
        if total_signals == 0:
            return None
            
        if bullish_signals > bearish_signals and bullish_signals >= 3:
            signal_type = "BUY"  # Will be reversed to SELL for contrarian
            strength = min(10.0, (bullish_signals / max(total_signals, 1)) * 10)
        elif bearish_signals > bullish_signals and bearish_signals >= 3:
            signal_type = "SELL"  # Will be reversed to BUY for contrarian
            strength = min(10.0, (bearish_signals / max(total_signals, 1)) * 10)
        else:
            return None
            
        # Apply ultra-strict filtering
        strength = self._apply_strict_filtering(strength, confluences, h1, h4, d1)
        
        if strength < self.config.MIN_SIGNAL_STRENGTH:
            return None
            
        return {
            'symbol': symbol,
            'signal': signal_type,
            'strength': round(strength, 1),
            'confluences': confluences,
            'timeframes': {
                'H1': h1,
                'H4': h4,
                'D1': d1
            }
        }
        
    def _apply_strict_filtering(self, base_strength, confluences, h1, h4, d1):
        """Apply ultra-strict filtering to signal strength."""
        strength = base_strength
        
        # Bonus for multiple confluences
        if len(confluences) >= 5:
            strength += 1.0
        elif len(confluences) >= 3:
            strength += 0.5
            
        # Penalty for weak signals
        if h1['rsi'] > 40 and h1['rsi'] < 60:  # RSI in neutral zone
            strength -= 1.0
            
        # Bonus for extreme RSI
        if h1['rsi'] > 75 or h1['rsi'] < 25:
            strength += 0.5
            
        # ATR volatility check
        if h1['atr'] < 0.0001:  # Too low volatility
            strength -= 2.0
            
        # Multi-timeframe alignment bonus
        rsi_alignment = abs(h1['rsi'] - h4['rsi']) < 10
        if rsi_alignment:
            strength += 0.5
            
        return max(0, min(10, strength))
        
    def _calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator."""
        if len(prices) < period + 1:
            return []
            
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gains = []
        avg_losses = []
        rsi_values = []
        
        # First RSI calculation
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        
        if avg_loss == 0:
            rsi_values.append(100)
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
            
        avg_gains.append(avg_gain)
        avg_losses.append(avg_loss)
        
        # Subsequent RSI calculations
        for i in range(period, len(deltas)):
            avg_gain = (avg_gains[-1] * (period - 1) + gains[i]) / period
            avg_loss = (avg_losses[-1] * (period - 1) + losses[i]) / period
            
            avg_gains.append(avg_gain)
            avg_losses.append(avg_loss)
            
            if avg_loss == 0:
                rsi_values.append(100)
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                rsi_values.append(rsi)
                
        return rsi_values
        
    def _calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average."""
        if len(prices) < period:
            return []
            
        ema_values = []
        multiplier = 2 / (period + 1)
        
        # Start with SMA
        sma = np.mean(prices[:period])
        ema_values.append(sma)
        
        # Calculate EMA
        for i in range(period, len(prices)):
            ema = (prices[i] * multiplier) + (ema_values[-1] * (1 - multiplier))
            ema_values.append(ema)
            
        return ema_values
        
    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD indicator."""
        if len(prices) < slow:
            return [], []
            
        ema_fast = self._calculate_ema(prices, fast)
        ema_slow = self._calculate_ema(prices, slow)
        
        # Align arrays
        min_len = min(len(ema_fast), len(ema_slow))
        if min_len == 0:
            return [], []
            
        ema_fast = ema_fast[-min_len:]
        ema_slow = ema_slow[-min_len:]
        
        macd_line = np.array(ema_fast) - np.array(ema_slow)
        macd_signal = self._calculate_ema(macd_line.tolist(), signal)
        
        return macd_line.tolist(), macd_signal
        
    def _calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands."""
        if len(prices) < period:
            return [], [], []
            
        upper_bands = []
        middle_bands = []
        lower_bands = []
        
        for i in range(period - 1, len(prices)):
            subset = prices[i - period + 1:i + 1]
            mean = np.mean(subset)
            std = np.std(subset)
            
            upper_bands.append(mean + (std * std_dev))
            middle_bands.append(mean)
            lower_bands.append(mean - (std * std_dev))
            
        return upper_bands, middle_bands, lower_bands
        
    def _calculate_atr(self, high, low, close, period=14):
        """Calculate Average True Range."""
        if len(high) < period + 1:
            return []
            
        true_ranges = []
        
        for i in range(1, len(high)):
            tr1 = high[i] - low[i]
            tr2 = abs(high[i] - close[i-1])
            tr3 = abs(low[i] - close[i-1])
            true_range = max(tr1, tr2, tr3)
            true_ranges.append(true_range)
            
        atr_values = []
        
        # First ATR (simple average)
        if len(true_ranges) >= period:
            atr = np.mean(true_ranges[:period])
            atr_values.append(atr)
            
            # Subsequent ATR (smoothed)
            for i in range(period, len(true_ranges)):
                atr = (atr * (period - 1) + true_ranges[i]) / period
                atr_values.append(atr)
                
        return atr_values
        
    def _find_support_resistance(self, high, low, close, window=5):
        """Find support and resistance levels."""
        if len(high) < window * 2:
            current_price = close[-1]
            return current_price * 0.99, current_price * 1.01
            
        # Find local minima and maxima
        support_levels = []
        resistance_levels = []
        
        for i in range(window, len(low) - window):
            # Check for support (local minimum)
            if all(low[i] <= low[j] for j in range(i - window, i + window + 1)):
                support_levels.append(low[i])
                
        for i in range(window, len(high) - window):
            # Check for resistance (local maximum)
            if all(high[i] >= high[j] for j in range(i - window, i + window + 1)):
                resistance_levels.append(high[i])
                
        # Get nearest levels
        current_price = close[-1]
        
        if support_levels:
            support = max([s for s in support_levels if s < current_price], default=current_price * 0.99)
        else:
            support = current_price * 0.99
            
        if resistance_levels:
            resistance = min([r for r in resistance_levels if r > current_price], default=current_price * 1.01)
        else:
            resistance = current_price * 1.01
            
        return support, resistance
    
    def _enhance_with_volume_analysis(self, symbol, signal_data):
        """
        Enhance signal with volume analysis for contrarian confirmation.
        
        Args:
            symbol (str): Currency pair
            signal_data (dict): Original signal data
            
        Returns:
            dict: Enhanced signal data with volume analysis
        """
        try:
            if not self.volume_analyzer:
                return signal_data
            
            # Get volume analysis for multiple timeframes
            volume_analysis = self.volume_analyzer.get_volume_contrarian_signals(
                symbol, ['M5', 'M15', 'H1']
            )
            
            if not volume_analysis or 'combined_analysis' not in volume_analysis:
                return signal_data
            
            combined_volume = volume_analysis['combined_analysis']
            volume_score = combined_volume['score']
            
            # Apply volume boost to signal strength
            original_strength = signal_data['strength']
            volume_boost = 0
            
            # Volume pattern bonuses for contrarian signals
            if volume_score >= 8.0:
                volume_boost = 1.5  # Strong volume confirmation
                signal_data['confluences'].append("Strong Volume Confirmation")
            elif volume_score >= 6.5:
                volume_boost = 1.0  # Moderate volume support
                signal_data['confluences'].append("Volume Support")
            elif volume_score >= 5.0:
                volume_boost = 0.5  # Neutral volume
            else:
                volume_boost = -1.0  # Volume against signal
                signal_data['confluences'].append("Volume Warning")
            
            # Check for specific volume patterns
            for tf in ['M5', 'M15', 'H1']:
                if tf in volume_analysis:
                    tf_analysis = volume_analysis[tf]
                    
                    # Volume spike bonus (exhaustion signal)
                    if tf_analysis.get('volume_spike', False):
                        volume_boost += 0.5
                        signal_data['confluences'].append(f"{tf} Volume Spike")
                    
                    # Price-volume divergence
                    if tf_analysis.get('price_volume_divergence', {}).get('detected', False):
                        divergence_type = tf_analysis['price_volume_divergence']['type']
                        if 'bearish' in divergence_type and signal_data['signal'] == 'BUY':
                            volume_boost += 1.0  # Bearish divergence supports contrarian BUY
                            signal_data['confluences'].append(f"{tf} Bearish Volume Divergence")
                        elif 'bullish' in divergence_type and signal_data['signal'] == 'SELL':
                            volume_boost += 1.0  # Bullish divergence supports contrarian SELL
                            signal_data['confluences'].append(f"{tf} Bullish Volume Divergence")
                    
                    # Exhaustion patterns
                    if tf_analysis.get('exhaustion_signal', {}).get('detected', False):
                        exhaustion_type = tf_analysis['exhaustion_signal']['type']
                        if 'buying_exhaustion' in exhaustion_type and signal_data['signal'] == 'BUY':
                            volume_boost += 1.5  # Buying exhaustion supports contrarian BUY (which becomes SELL)
                            signal_data['confluences'].append(f"{tf} Buying Exhaustion")
                        elif 'selling_exhaustion' in exhaustion_type and signal_data['signal'] == 'SELL':
                            volume_boost += 1.5  # Selling exhaustion supports contrarian SELL (which becomes BUY)
                            signal_data['confluences'].append(f"{tf} Selling Exhaustion")
            
            # Apply volume enhancement
            enhanced_strength = min(10.0, original_strength + volume_boost)
            
            # Add volume data to signal
            signal_data['strength'] = enhanced_strength
            signal_data['volume_score'] = volume_score
            signal_data['volume_boost'] = volume_boost
            signal_data['volume_analysis'] = volume_analysis
            signal_data['volume_recommendation'] = combined_volume.get('recommendation', {})
            
            # Volume-based filtering
            if volume_score < 3.0 and enhanced_strength < 8.0:
                # Poor volume pattern - downgrade signal significantly
                print(f"⚠️ Volume analysis suggests avoiding {symbol} (Volume Score: {volume_score:.1f})")
                return None
            
            print(f"🔊 Volume enhancement: {original_strength:.1f} → {enhanced_strength:.1f} (+{volume_boost:.1f})")
            
            return signal_data
            
        except Exception as e:
            print(f"❌ Volume enhancement error for {symbol}: {e}")
            return signal_data


def main():
    """Test the signal generator."""
    print("📊 Signal Generator Test")
    print("This module generates signals for contrarian trading")


if __name__ == "__main__":
    main()
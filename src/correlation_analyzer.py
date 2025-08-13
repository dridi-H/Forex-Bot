"""
Advanced Correlation Analysis Module

Analyzes currency pair correlations to prevent over-exposure to correlated pairs
and optimize portfolio diversification.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import os


class CorrelationAnalyzer:
    """
    Advanced Correlation Analysis System
    
    Monitors and analyzes correlations between currency pairs to:
    - Prevent trading highly correlated pairs simultaneously
    - Optimize portfolio diversification
    - Provide correlation-based trade filtering
    """
    
    def __init__(self, mt5_connector=None):
        """Initialize Correlation Analyzer."""
        self.mt5 = mt5_connector
        self.correlation_matrix = {}
        self.correlation_history = {}
        self.correlation_threshold = 0.7  # High correlation threshold
        self.lookback_periods = {
            'short': 100,   # 100 bars for short-term correlation
            'medium': 500,  # 500 bars for medium-term correlation
            'long': 1000    # 1000 bars for long-term correlation
        }
        self.cache_file = "correlation_cache.json"
        
        # Major currency pairs to analyze
        self.major_pairs = [
            'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 
            'USDCHF', 'USDCAD', 'NZDUSD', 'EURJPY',
            'GBPJPY', 'EURGBP', 'AUDJPY', 'EURAUD'
        ]
        
        print("📊 Advanced Correlation Analyzer initialized")
        self._load_correlation_cache()
    
    def analyze_correlations(self, timeframe='H1', update_cache=True):
        """
        Analyze correlations between all major currency pairs.
        
        Args:
            timeframe (str): Timeframe for correlation analysis
            update_cache (bool): Whether to update the correlation cache
            
        Returns:
            dict: Correlation analysis results
        """
        try:
            print(f"📊 Analyzing correlations for {timeframe} timeframe...")
            
            # Get price data for all pairs
            price_data = self._get_price_data(timeframe)
            
            if not price_data:
                print("❌ No price data available for correlation analysis")
                return {}
            
            # Calculate correlations for different periods
            correlations = {}
            for period_name, period_length in self.lookback_periods.items():
                correlations[period_name] = self._calculate_correlation_matrix(
                    price_data, period_length
                )
            
            # Update correlation matrix with weighted average
            self.correlation_matrix = self._calculate_weighted_correlation(correlations)
            
            # Analyze correlation patterns
            analysis_results = {
                'correlation_matrix': self.correlation_matrix,
                'high_correlations': self._find_high_correlations(),
                'correlation_clusters': self._identify_correlation_clusters(),
                'diversification_score': self._calculate_diversification_score(),
                'timestamp': datetime.now().isoformat(),
                'timeframe': timeframe
            }
            
            # Update cache if requested
            if update_cache:
                self._update_correlation_cache(analysis_results)
            
            # Log analysis summary
            self._log_correlation_summary(analysis_results)
            
            return analysis_results
            
        except Exception as e:
            print(f"❌ Correlation analysis error: {e}")
            return {}
    
    def _get_price_data(self, timeframe='H1'):
        """Get price data for all major pairs."""
        price_data = {}
        
        if not self.mt5:
            print("⚠️ No MT5 connector available for correlation analysis")
            return {}
        
        try:
            max_bars = max(self.lookback_periods.values()) + 50  # Extra buffer
            
            for pair in self.major_pairs:
                try:
                    bars = self.mt5.get_rates(pair, timeframe, max_bars)
                    
                    if bars and len(bars) > 100:  # Minimum data requirement
                        # Extract close prices
                        closes = [bar['close'] for bar in bars]
                        price_data[pair] = closes
                        print(f"   ✅ {pair}: {len(closes)} bars")
                    else:
                        print(f"   ⚠️ {pair}: Insufficient data")
                        
                except Exception as e:
                    print(f"   ❌ {pair}: Error getting data - {e}")
                    continue
            
            return price_data
            
        except Exception as e:
            print(f"❌ Price data error: {e}")
            return {}
    
    def _calculate_correlation_matrix(self, price_data, period_length):
        """Calculate correlation matrix for given period."""
        try:
            correlations = {}
            pairs = list(price_data.keys())
            
            for i, pair1 in enumerate(pairs):
                correlations[pair1] = {}
                
                for j, pair2 in enumerate(pairs):
                    if pair1 == pair2:
                        correlations[pair1][pair2] = 1.0
                    else:
                        # Get recent price data
                        prices1 = price_data[pair1][-period_length:]
                        prices2 = price_data[pair2][-period_length:]
                        
                        # Calculate returns
                        returns1 = self._calculate_returns(prices1)
                        returns2 = self._calculate_returns(prices2)
                        
                        # Calculate correlation
                        min_length = min(len(returns1), len(returns2))
                        if min_length > 20:  # Minimum for meaningful correlation
                            corr = np.corrcoef(
                                returns1[-min_length:], 
                                returns2[-min_length:]
                            )[0, 1]
                            
                            correlations[pair1][pair2] = round(corr, 4)
                        else:
                            correlations[pair1][pair2] = 0.0
            
            return correlations
            
        except Exception as e:
            print(f"❌ Correlation matrix error: {e}")
            return {}
    
    def _calculate_returns(self, prices):
        """Calculate price returns from price series."""
        try:
            if len(prices) < 2:
                return []
            
            returns = []
            for i in range(1, len(prices)):
                if prices[i-1] != 0:
                    ret = (prices[i] - prices[i-1]) / prices[i-1]
                    returns.append(ret)
            
            return returns
            
        except Exception:
            return []
    
    def _calculate_weighted_correlation(self, correlations):
        """Calculate weighted average correlation across different periods."""
        try:
            if not correlations:
                return {}
            
            # Weights for different periods (short-term weighted more)
            weights = {
                'short': 0.5,   # 50% weight to short-term
                'medium': 0.3,  # 30% weight to medium-term
                'long': 0.2     # 20% weight to long-term
            }
            
            weighted_corr = {}
            pairs = list(correlations['short'].keys()) if 'short' in correlations else []
            
            for pair1 in pairs:
                weighted_corr[pair1] = {}
                
                for pair2 in pairs:
                    weighted_value = 0.0
                    total_weight = 0.0
                    
                    for period, weight in weights.items():
                        if period in correlations and pair1 in correlations[period]:
                            if pair2 in correlations[period][pair1]:
                                corr_value = correlations[period][pair1][pair2]
                                if not np.isnan(corr_value):
                                    weighted_value += corr_value * weight
                                    total_weight += weight
                    
                    if total_weight > 0:
                        weighted_corr[pair1][pair2] = round(weighted_value / total_weight, 4)
                    else:
                        weighted_corr[pair1][pair2] = 0.0
            
            return weighted_corr
            
        except Exception as e:
            print(f"❌ Weighted correlation error: {e}")
            return {}
    
    def _find_high_correlations(self):
        """Find pairs with high correlation above threshold."""
        high_correlations = []
        
        try:
            if not self.correlation_matrix:
                return high_correlations
            
            pairs = list(self.correlation_matrix.keys())
            
            for i, pair1 in enumerate(pairs):
                for j, pair2 in enumerate(pairs[i+1:], i+1):
                    if pair1 in self.correlation_matrix and pair2 in self.correlation_matrix[pair1]:
                        corr = abs(self.correlation_matrix[pair1][pair2])
                        
                        if corr >= self.correlation_threshold:
                            high_correlations.append({
                                'pair1': pair1,
                                'pair2': pair2,
                                'correlation': round(corr, 4),
                                'type': 'positive' if self.correlation_matrix[pair1][pair2] > 0 else 'negative'
                            })
            
            # Sort by correlation strength
            high_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            
            return high_correlations
            
        except Exception as e:
            print(f"❌ High correlation analysis error: {e}")
            return []
    
    def _identify_correlation_clusters(self):
        """Identify clusters of highly correlated pairs."""
        try:
            clusters = []
            high_corrs = self._find_high_correlations()
            
            if not high_corrs:
                return clusters
            
            # Group highly correlated pairs into clusters
            processed_pairs = set()
            
            for corr_data in high_corrs:
                pair1 = corr_data['pair1']
                pair2 = corr_data['pair2']
                
                if pair1 not in processed_pairs and pair2 not in processed_pairs:
                    # Start new cluster
                    cluster = {
                        'pairs': [pair1, pair2],
                        'avg_correlation': abs(corr_data['correlation']),
                        'type': corr_data['type']
                    }
                    
                    # Find other pairs that correlate with this cluster
                    for other_corr in high_corrs:
                        other_pair1 = other_corr['pair1']
                        other_pair2 = other_corr['pair2']
                        
                        if (other_pair1 in cluster['pairs'] and other_pair2 not in cluster['pairs']):
                            cluster['pairs'].append(other_pair2)
                        elif (other_pair2 in cluster['pairs'] and other_pair1 not in cluster['pairs']):
                            cluster['pairs'].append(other_pair1)
                    
                    clusters.append(cluster)
                    processed_pairs.update(cluster['pairs'])
            
            return clusters
            
        except Exception as e:
            print(f"❌ Cluster analysis error: {e}")
            return []
    
    def _calculate_diversification_score(self):
        """Calculate overall portfolio diversification score (0-100)."""
        try:
            if not self.correlation_matrix:
                return 50.0  # Neutral score
            
            pairs = list(self.correlation_matrix.keys())
            total_correlations = 0
            correlation_count = 0
            
            for i, pair1 in enumerate(pairs):
                for j, pair2 in enumerate(pairs[i+1:], i+1):
                    if pair1 in self.correlation_matrix and pair2 in self.correlation_matrix[pair1]:
                        corr = abs(self.correlation_matrix[pair1][pair2])
                        total_correlations += corr
                        correlation_count += 1
            
            if correlation_count == 0:
                return 50.0
            
            avg_correlation = total_correlations / correlation_count
            
            # Convert to diversification score (lower correlation = higher diversification)
            diversification_score = (1 - avg_correlation) * 100
            
            return max(0, min(100, round(diversification_score, 1)))
            
        except Exception as e:
            print(f"❌ Diversification score error: {e}")
            return 50.0
    
    def check_correlation_conflict(self, pair1, pair2):
        """
        Check if two pairs have high correlation conflict.
        
        Args:
            pair1 (str): First currency pair
            pair2 (str): Second currency pair
            
        Returns:
            dict: Correlation conflict analysis
        """
        try:
            if not self.correlation_matrix:
                self.analyze_correlations()
            
            if (pair1 not in self.correlation_matrix or 
                pair2 not in self.correlation_matrix[pair1]):
                return {
                    'has_conflict': False,
                    'correlation': 0.0,
                    'message': 'No correlation data available'
                }
            
            correlation = self.correlation_matrix[pair1][pair2]
            abs_correlation = abs(correlation)
            
            has_conflict = abs_correlation >= self.correlation_threshold
            
            if has_conflict:
                conflict_type = 'positive' if correlation > 0 else 'negative'
                message = f"High {conflict_type} correlation: {correlation:.3f}"
            else:
                message = f"Low correlation: {correlation:.3f} - Safe to trade together"
            
            return {
                'has_conflict': has_conflict,
                'correlation': round(correlation, 4),
                'correlation_strength': abs_correlation,
                'conflict_type': 'positive' if correlation > 0 else 'negative',
                'message': message,
                'recommendation': 'AVOID' if has_conflict else 'ALLOW'
            }
            
        except Exception as e:
            print(f"❌ Correlation conflict check error: {e}")
            return {
                'has_conflict': False,
                'correlation': 0.0,
                'message': f'Error: {e}'
            }
    
    def get_safe_pairs_for_trading(self, current_pairs):
        """
        Get list of pairs safe to trade alongside current positions.
        
        Args:
            current_pairs (list): List of currently traded pairs
            
        Returns:
            list: List of pairs safe to trade
        """
        try:
            if not current_pairs:
                return self.major_pairs.copy()
            
            safe_pairs = []
            
            for candidate_pair in self.major_pairs:
                if candidate_pair in current_pairs:
                    continue
                
                is_safe = True
                
                for current_pair in current_pairs:
                    conflict_check = self.check_correlation_conflict(
                        candidate_pair, current_pair
                    )
                    
                    if conflict_check['has_conflict']:
                        is_safe = False
                        break
                
                if is_safe:
                    safe_pairs.append(candidate_pair)
            
            return safe_pairs
            
        except Exception as e:
            print(f"❌ Safe pairs analysis error: {e}")
            return []
    
    def _load_correlation_cache(self):
        """Load correlation data from cache file."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cached_data = json.load(f)
                    
                    if 'correlation_matrix' in cached_data:
                        self.correlation_matrix = cached_data['correlation_matrix']
                        print("📥 Loaded correlation cache")
                    
        except Exception as e:
            print(f"⚠️ Could not load correlation cache: {e}")
    
    def _update_correlation_cache(self, analysis_results):
        """Update correlation cache with latest analysis."""
        try:
            cache_data = {
                'correlation_matrix': self.correlation_matrix,
                'last_update': datetime.now().isoformat(),
                'analysis_results': analysis_results
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            print("💾 Updated correlation cache")
            
        except Exception as e:
            print(f"❌ Cache update error: {e}")
    
    def _log_correlation_summary(self, analysis_results):
        """Log correlation analysis summary."""
        try:
            print(f"\n📊 Correlation Analysis Summary:")
            print(f"   🔗 High Correlations: {len(analysis_results.get('high_correlations', []))}")
            print(f"   🎯 Diversification Score: {analysis_results.get('diversification_score', 0):.1f}%")
            print(f"   📊 Correlation Clusters: {len(analysis_results.get('correlation_clusters', []))}")
            
            # Show top correlations
            high_corrs = analysis_results.get('high_correlations', [])[:5]
            if high_corrs:
                print(f"   📈 Top Correlations:")
                for corr in high_corrs:
                    print(f"     • {corr['pair1']} vs {corr['pair2']}: {corr['correlation']:.3f}")
            
        except Exception as e:
            print(f"❌ Logging error: {e}")
    
    def get_correlation_stats(self):
        """Get comprehensive correlation statistics."""
        try:
            if not self.correlation_matrix:
                return {'error': 'No correlation data available'}
            
            stats = {
                'pairs_analyzed': len(self.correlation_matrix),
                'high_correlations_count': len(self._find_high_correlations()),
                'diversification_score': self._calculate_diversification_score(),
                'correlation_threshold': self.correlation_threshold,
                'last_analysis': datetime.now().isoformat(),
                'major_pairs': self.major_pairs
            }
            
            return stats
            
        except Exception as e:
            print(f"❌ Stats error: {e}")
            return {'error': str(e)}

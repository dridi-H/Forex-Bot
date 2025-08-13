"""
Advanced Machine Learning Signal Enhancement Module

Provides institutional-grade ML signal enhancement with ensemble models,
continuous learning, and sophisticated feature engineering.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import joblib
import json

# Enhanced ML imports with fallback
try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.neural_network import MLPRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler, RobustScaler
    from sklearn.model_selection import train_test_split, cross_val_score, TimeSeriesSplit
    from sklearn.metrics import mean_squared_error, r2_score
    ML_AVAILABLE = True
    print("✅ Advanced ML libraries loaded successfully")
except ImportError as e:
    print(f"⚠️ ML libraries not available: {e}")
    print("📋 Install with: pip install scikit-learn pandas")
    ML_AVAILABLE = False


class MLSignalEnhancer:
    """
    Advanced Machine Learning Signal Enhancement System
    
    Enhances signal quality through ensemble ML models and continuous learning.
    """
    
    def __init__(self, mt5_connector=None):
        """Initialize Advanced ML Signal Enhancer."""
        self.mt5 = mt5_connector
        self.models = {}
        self.scalers = {}
        self.feature_history = {}
        self.performance_history = {}
        self.ml_available = ML_AVAILABLE
        self.model_path = "models/"
        
        # Ensure models directory exists
        os.makedirs(self.model_path, exist_ok=True)
        
        print(f"🤖 Advanced ML Signal Enhancer: {'✅ ENABLED' if self.ml_available else '❌ FALLBACK MODE'}")
        
        if self.ml_available:
            self._initialize_ensemble_models()
            self._load_pretrained_models()
    
    def _initialize_ensemble_models(self):
        """Initialize ensemble of ML models for better predictions."""
        if not self.ml_available:
            return
            
        # Ensemble models for signal strength prediction
        self.model_templates = {
            'rf': RandomForestRegressor(
                n_estimators=200,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            ),
            'gb': GradientBoostingRegressor(
                n_estimators=150,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            ),
            'mlp': MLPRegressor(
                hidden_layer_sizes=(100, 50),
                max_iter=1000,
                random_state=42,
                early_stopping=True
            ),
            'linear': LinearRegression()
        }
        
        # Scaler options
        self.scaler_types = {
            'standard': StandardScaler(),
            'robust': RobustScaler()
        }
    
    def _load_pretrained_models(self):
        """Load pre-trained models if available."""
        try:
            for symbol in ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCHF', 'USDCAD', 'NZDUSD']:
                model_file = os.path.join(self.model_path, f"{symbol}_ensemble.pkl")
                if os.path.exists(model_file):
                    self.models[symbol] = joblib.load(model_file)
                    print(f"📥 Loaded pre-trained models for {symbol}")
        except Exception as e:
            print(f"⚠️ Could not load pre-trained models: {e}")
    
    def enhance_signal(self, symbol, signal_data):
        """
        Enhance signal using advanced ML ensemble.
        
        Args:
            symbol (str): Currency pair symbol
            signal_data (dict): Original signal data
            
        Returns:
            dict: Enhanced signal data with ML scores
        """
        if not signal_data:
            return signal_data
        
        try:
            # Extract comprehensive features
            features = self._extract_advanced_features(symbol, signal_data)
            
            # Get ensemble ML prediction
            ml_scores = self._get_ensemble_prediction(symbol, features)
            
            # Calculate enhanced signal strength
            original_strength = signal_data.get('strength', 0)
            enhanced_strength = self._combine_ml_scores(original_strength, ml_scores)
            
            # Calculate confidence and reliability
            confidence = self._calculate_ml_confidence(ml_scores, features)
            reliability = self._assess_signal_reliability(symbol, features)
            
            # Create enhanced signal data
            enhanced_signal = signal_data.copy()
            enhanced_signal.update({
                'ml_scores': ml_scores,
                'original_strength': original_strength,
                'strength': enhanced_strength,
                'ml_confidence': confidence,
                'ml_reliability': reliability,
                'enhancement_factor': enhanced_strength / max(original_strength, 0.1),
                'ml_features_count': len(features),
                'ml_timestamp': datetime.now()
            })
            
            # Log enhancement details
            self._log_enhancement(symbol, original_strength, enhanced_strength, ml_scores, confidence)
            
            return enhanced_signal
            
        except Exception as e:
            print(f"❌ ML Enhancement error for {symbol}: {e}")
            return signal_data
    
    def _extract_advanced_features(self, symbol, signal_data):
        """Extract comprehensive feature set for ML models."""
        features = []
        
        try:
            # 1. Basic signal features (5 features)
            features.extend([
                signal_data.get('strength', 0),
                len(signal_data.get('confluences', [])),
                signal_data.get('rsi_h1', 50) / 100,  # Normalize to 0-1
                signal_data.get('rsi_h4', 50) / 100,
                signal_data.get('rsi_d1', 50) / 100,
            ])
            
            # 2. Market structure features (8 features)
            market_data = self._get_enhanced_market_data(symbol)
            if market_data:
                features.extend(self._extract_market_features(market_data))
            else:
                features.extend([0] * 8)
            
            # 3. Time-based features (6 features)
            features.extend(self._extract_time_features())
            
            # 4. Volatility and momentum features (4 features)
            features.extend(self._extract_volatility_features(symbol))
            
            # 5. Inter-market features (2 features)
            features.extend(self._extract_intermarket_features(symbol))
            
            # Ensure consistent feature count (25 features total)
            while len(features) < 25:
                features.append(0)
            
            return np.array(features[:25])
            
        except Exception as e:
            print(f"❌ Feature extraction error: {e}")
            return np.zeros(25)
    
    def _get_enhanced_market_data(self, symbol):
        """Get enhanced market data for feature extraction."""
        if not self.mt5:
            return None
            
        try:
            market_data = {}
            timeframes = ['H1', 'H4', 'D1']
            
            for tf in timeframes:
                count = {'H1': 100, 'H4': 50, 'D1': 30}[tf]
                bars = self.mt5.get_rates(symbol, tf, count)
                
                if bars is not None and len(bars) > 0:
                    market_data[tf] = bars
                else:
                    market_data[tf] = []
            
            return market_data
            
        except Exception as e:
            print(f"❌ Market data error: {e}")
            return None
    
    def _extract_market_features(self, market_data):
        """Extract market structure features from price data."""
        features = []
        
        try:
            # H1 features
            h1_data = market_data.get('H1', [])
            if len(h1_data) > 20:
                closes = [bar['close'] for bar in h1_data[-20:]]
                highs = [bar['high'] for bar in h1_data[-20:]]
                lows = [bar['low'] for bar in h1_data[-20:]]
                
                features.extend([
                    np.std(closes) / np.mean(closes),  # Coefficient of variation
                    (closes[-1] - closes[0]) / closes[0],  # Price momentum
                    (max(highs) - min(lows)) / np.mean(closes),  # Range ratio
                ])
            else:
                features.extend([0, 0, 0])
            
            # H4 features  
            h4_data = market_data.get('H4', [])
            if len(h4_data) > 10:
                closes = [bar['close'] for bar in h4_data[-10:]]
                features.extend([
                    np.std(closes) / np.mean(closes),  # H4 volatility
                    (closes[-1] - closes[-5]) / closes[-5] if len(closes) >= 5 else 0,  # Short momentum
                ])
            else:
                features.extend([0, 0])
            
            # D1 features
            d1_data = market_data.get('D1', [])
            if len(d1_data) > 5:
                closes = [bar['close'] for bar in d1_data[-5:]]
                features.extend([
                    (closes[-1] - closes[0]) / closes[0],  # Weekly trend
                    np.std(closes) / np.mean(closes),  # Weekly volatility
                    len([c for c in closes if c > closes[0]]) / len(closes),  # Bullish ratio
                ])
            else:
                features.extend([0, 0, 0])
            
            return features
            
        except Exception as e:
            print(f"❌ Market features error: {e}")
            return [0] * 8
    
    def _extract_time_features(self):
        """Extract time-based features."""
        now = datetime.utcnow()
        
        return [
            now.hour / 24,  # Hour normalized
            now.weekday() / 6,  # Weekday normalized
            1 if 8 <= now.hour <= 16 else 0,  # London session
            1 if 13 <= now.hour <= 21 else 0,  # NY session
            1 if now.weekday() < 5 else 0,  # Weekday
            np.sin(2 * np.pi * now.hour / 24),  # Cyclical hour
        ]
    
    def _extract_volatility_features(self, symbol):
        """Extract volatility and momentum features."""
        try:
            if not self.mt5:
                return [0] * 4
            
            # Get recent tick data for volatility analysis
            tick = self.mt5.get_tick(symbol)
            if not tick:
                return [0] * 4
            
            # Simple volatility proxies
            spread = abs(tick.ask - tick.bid) / tick.bid if tick.bid > 0 else 0
            
            return [
                spread * 10000,  # Spread in pips
                tick.volume if hasattr(tick, 'volume') else 0,  # Volume
                0,  # Placeholder for ATR
                0,  # Placeholder for momentum
            ]
            
        except Exception:
            return [0] * 4
    
    def _extract_intermarket_features(self, symbol):
        """Extract inter-market correlation features."""
        # Simplified inter-market features
        return [
            0.5,  # Placeholder for USD strength index
            0.5,  # Placeholder for risk sentiment
        ]
    
    def _get_ensemble_prediction(self, symbol, features):
        """Get prediction from ensemble of ML models."""
        if not self.ml_available:
            return self._fallback_prediction(features)
        
        try:
            predictions = {}
            
            # If trained models exist for this symbol
            if symbol in self.models:
                ensemble = self.models[symbol]
                
                for model_name, model_data in ensemble.items():
                    if 'model' in model_data and 'scaler' in model_data:
                        scaler = model_data['scaler']
                        model = model_data['model']
                        
                        # Scale features and predict
                        scaled_features = scaler.transform([features])
                        pred = model.predict(scaled_features)[0]
                        predictions[model_name] = max(0, min(10, pred))
            
            # If no trained models, use feature-based prediction
            if not predictions:
                predictions = self._feature_based_prediction(features)
            
            return predictions
            
        except Exception as e:
            print(f"❌ Ensemble prediction error: {e}")
            return self._fallback_prediction(features)
    
    def _feature_based_prediction(self, features):
        """Generate predictions based on feature analysis."""
        try:
            base_score = features[0] if len(features) > 0 else 5.0  # Original strength
            confluences = features[1] if len(features) > 1 else 0
            
            # Different prediction approaches
            predictions = {
                'feature_enhanced': min(10, base_score + confluences * 0.3),
                'rsi_adjusted': self._rsi_adjustment(base_score, features[2:5] if len(features) > 4 else [0.5, 0.5, 0.5]),
                'volatility_adjusted': self._volatility_adjustment(base_score, features[13:17] if len(features) > 16 else [0, 0, 0, 0]),
                'time_adjusted': self._time_adjustment(base_score, features[5:11] if len(features) > 10 else [0] * 6),
            }
            
            return predictions
            
        except Exception as e:
            print(f"❌ Feature prediction error: {e}")
            return self._fallback_prediction(features)
    
    def _rsi_adjustment(self, base_score, rsi_features):
        """Adjust score based on RSI analysis."""
        try:
            avg_rsi = np.mean(rsi_features) * 100
            
            # Bonus for extreme RSI levels
            if avg_rsi < 30 or avg_rsi > 70:
                return min(10, base_score + 1.5)
            elif avg_rsi < 40 or avg_rsi > 60:
                return min(10, base_score + 0.5)
            else:
                return base_score
                
        except Exception:
            return base_score
    
    def _volatility_adjustment(self, base_score, vol_features):
        """Adjust score based on volatility analysis."""
        try:
            if vol_features[0] > 0:  # Has spread data
                return min(10, base_score + 0.3)
            return base_score
        except Exception:
            return base_score
    
    def _time_adjustment(self, base_score, time_features):
        """Adjust score based on time analysis."""
        try:
            # Bonus during active trading sessions
            if len(time_features) > 2 and (time_features[2] or time_features[3]):
                return min(10, base_score + 0.5)
            return base_score
        except Exception:
            return base_score
    
    def _fallback_prediction(self, features):
        """Fallback prediction when ML is not available."""
        try:
            base_strength = features[0] if len(features) > 0 else 5.0
            return {
                'fallback': max(0, min(10, base_strength + 0.5))
            }
        except Exception:
            return {'fallback': 5.0}
    
    def _combine_ml_scores(self, original, ml_scores):
        """Combine original signal with ML ensemble predictions."""
        try:
            if not ml_scores:
                return original
            
            # Calculate weighted average of ML predictions
            ml_avg = np.mean(list(ml_scores.values()))
            
            # Combine: 50% original, 50% ML average
            combined = (original * 0.5) + (ml_avg * 0.5)
            
            return max(0, min(10, combined))
            
        except Exception:
            return original
    
    def _calculate_ml_confidence(self, ml_scores, features):
        """Calculate confidence level for ML predictions."""
        try:
            base_confidence = 60.0
            
            # Higher confidence with more models agreeing
            if len(ml_scores) > 1:
                scores = list(ml_scores.values())
                std_dev = np.std(scores)
                agreement_bonus = max(0, 20 - std_dev * 4)
                base_confidence += agreement_bonus
            
            # Feature quality bonus
            if len(features) > 1 and features[1] >= 3:  # Good confluences
                base_confidence += 10
            
            # Session timing bonus
            if len(features) > 7 and (features[7] or features[8]):
                base_confidence += 5
            
            return max(0, min(100, base_confidence))
            
        except Exception:
            return 60.0
    
    def _assess_signal_reliability(self, symbol, features):
        """Assess overall signal reliability."""
        try:
            reliability = 50.0
            
            # Historical performance bonus
            if symbol in self.performance_history:
                recent_performance = self._get_recent_performance(symbol)
                if recent_performance > 60:
                    reliability += 20
                elif recent_performance > 40:
                    reliability += 10
            
            # Feature completeness bonus
            non_zero_features = np.count_nonzero(features)
            completeness_bonus = (non_zero_features / len(features)) * 20
            reliability += completeness_bonus
            
            return max(0, min(100, reliability))
            
        except Exception:
            return 50.0
    
    def _get_recent_performance(self, symbol):
        """Get recent performance percentage for symbol."""
        try:
            if symbol not in self.performance_history:
                return 50.0
            
            recent = self.performance_history[symbol][-50:]  # Last 50 predictions
            if not recent:
                return 50.0
            
            successes = sum(1 for p in recent if p.get('outcome', 0) > 0)
            return (successes / len(recent)) * 100
            
        except Exception:
            return 50.0
    
    def _log_enhancement(self, symbol, original, enhanced, ml_scores, confidence):
        """Log ML enhancement details."""
        try:
            improvement = ((enhanced - original) / max(original, 0.1)) * 100
            
            print(f"🤖 ML Enhancement [{symbol}]:")
            print(f"   📊 Original: {original:.1f}/10")
            print(f"   🧠 Enhanced: {enhanced:.1f}/10")
            print(f"   📈 Improvement: {improvement:+.1f}%")
            print(f"   🎯 Confidence: {confidence:.1f}%")
            print(f"   🔢 Models: {len(ml_scores)}")
            
        except Exception as e:
            print(f"❌ Logging error: {e}")
    
    def train_models(self, symbol, training_data):
        """Train ensemble models for a specific symbol."""
        if not self.ml_available or len(training_data) < 100:
            print(f"⚠️ Insufficient data to train models for {symbol}")
            return False
        
        try:
            print(f"🤖 Training ensemble models for {symbol}...")
            
            # Prepare training data
            X = np.array([d['features'] for d in training_data])
            y = np.array([d['outcome'] for d in training_data])
            
            # Initialize ensemble for this symbol
            self.models[symbol] = {}
            
            # Train each model in ensemble
            for model_name, model_template in self.model_templates.items():
                try:
                    # Initialize scaler and model
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    
                    # Create fresh model instance
                    model = model_template.__class__(**model_template.get_params())
                    
                    # Train with cross-validation
                    cv = TimeSeriesSplit(n_splits=5)
                    cv_scores = cross_val_score(model, X_scaled, y, cv=cv, scoring='r2')
                    
                    # Train on full dataset
                    model.fit(X_scaled, y)
                    
                    # Store model and scaler
                    self.models[symbol][model_name] = {
                        'model': model,
                        'scaler': scaler,
                        'cv_score': cv_scores.mean(),
                        'cv_std': cv_scores.std()
                    }
                    
                    print(f"   ✅ {model_name.upper()}: CV R² = {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
                    
                except Exception as e:
                    print(f"   ❌ Failed to train {model_name}: {e}")
            
            # Save ensemble models
            self._save_models(symbol)
            
            return len(self.models[symbol]) > 0
            
        except Exception as e:
            print(f"❌ Training error for {symbol}: {e}")
            return False
    
    def _save_models(self, symbol):
        """Save trained models to disk."""
        try:
            model_file = os.path.join(self.model_path, f"{symbol}_ensemble.pkl")
            joblib.dump(self.models[symbol], model_file)
            print(f"💾 Saved models for {symbol}")
        except Exception as e:
            print(f"❌ Save error: {e}")
    
    def update_performance(self, symbol, signal_data, outcome):
        """Update performance history for continuous learning."""
        try:
            if symbol not in self.performance_history:
                self.performance_history[symbol] = []
            
            performance_record = {
                'timestamp': datetime.now(),
                'original_strength': signal_data.get('original_strength', 0),
                'enhanced_strength': signal_data.get('strength', 0),
                'ml_confidence': signal_data.get('ml_confidence', 0),
                'outcome': outcome,  # Success/failure score
                'features': signal_data.get('ml_features_count', 0)
            }
            
            self.performance_history[symbol].append(performance_record)
            
            # Keep recent history only
            if len(self.performance_history[symbol]) > 1000:
                self.performance_history[symbol] = self.performance_history[symbol][-1000:]
            
            print(f"📊 Updated ML performance for {symbol} (outcome: {outcome})")
            
        except Exception as e:
            print(f"❌ Performance update error: {e}")
    
    def get_enhancement_stats(self):
        """Get overall ML enhancement statistics."""
        try:
            stats = {
                'symbols_with_models': len(self.models),
                'ml_available': self.ml_available,
                'total_predictions': sum(len(hist) for hist in self.performance_history.values()),
                'model_types': list(self.model_templates.keys()) if self.ml_available else [],
            }
            
            # Calculate average performance by symbol
            performance_by_symbol = {}
            for symbol, history in self.performance_history.items():
                if history:
                    recent = history[-100:]
                    avg_outcome = np.mean([h['outcome'] for h in recent])
                    performance_by_symbol[symbol] = avg_outcome
            
            stats['performance_by_symbol'] = performance_by_symbol
            
            return stats
            
        except Exception as e:
            print(f"❌ Stats error: {e}")
            return {'error': str(e)}

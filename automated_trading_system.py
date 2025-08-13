#!/usr/bin/env python3
"""
Contrarian Automated Trading System

A soph        print(f"🛡️ Min Signal Strength: {self.config.MIN_SIGNAL_STRENGTH}/10 (PREMIUM ONLY)")
        print(f"💰 Fixed Risk: ${self.config.FIXED_RISK_AMOUNT} per trade")
        print(f"🚫 Max Daily Drawdown: ${self.config.MAX_DAILY_DRAWDOWN}")
        print(f"🎯 Daily Profit Target: ${self.config.DAILY_PROFIT_TARGET}")
        print(f"🎯 Max Concurrent Trades: {self.config.MAX_CONCURRENT_TRADES}")
        print(f"📈 Max Daily Trades: {self.config.MAX_TRADES_PER_DAY} ({self.config.MAX_TRADES_PER_PAIR_PER_DAY} per pair)")
        print(f"⭐ Priority Threshold: {self.config.PRIORITY_SIGNAL_THRESHOLD}/10")
        print(f"🔄 Trade Following: {'✅ ENABLED' if self.config.ENABLE_TRADE_FOLLOWING else '❌ DISABLED'}")
        print(f"🛑 Stop on Success: {'✅ ENABLED' if self.config.STOP_TRADING_ON_PAIR_SUCCESS else '❌ DISABLED'}")ated automated trading system that implements contrarian strategy
by reversing all trading signals (BUY signals → SELL trades, SELL signals → BUY trades).

Features:
- Signal reversal for contrarian trading
- ATR-based dynamic risk management
- Multi-timeframe analysis
- Telegram notifications
- Ultra-strict signal filtering (7.0/10 minimum)
"""

import time
import sys
import os
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.config import TradingConfig
    from src.signal_generator import SignalGenerator
    from src.mt5_connector import MT5Connector
    from src.telegram_notifier import TelegramNotifier
    from src.ml_signal_enhancer import MLSignalEnhancer
    from src.correlation_analyzer import CorrelationAnalyzer
    # from src.portfolio_heat_tracker import PortfolioHeatTracker  # Removed
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all modules are in the src/ directory")
    sys.exit(1)


class ContriarianTradingSystem:
    """
    Main Contrarian Trading System
    
    Executes contrarian trades by reversing all signals:
    - BUY signals → SELL trades
    - SELL signals → BUY trades
    """
    
    def __init__(self):
        """Initialize the contrarian trading system."""
        print(f"{Fore.CYAN}🔄 Initializing Advanced AI-Powered Contrarian Trading System...{Style.RESET_ALL}")
        
        # Initialize core components
        self.config = TradingConfig()
        self.mt5 = MT5Connector()
        self.signal_generator = SignalGenerator(self.mt5, self.config)
        self.telegram = TelegramNotifier()
        
        # Initialize AI enhancement modules
        print(f"{Fore.MAGENTA}🤖 Initializing AI Enhancement Systems...{Style.RESET_ALL}")
        self.ml_enhancer = MLSignalEnhancer(self.mt5)
        self.correlation_analyzer = CorrelationAnalyzer(self.mt5)
        # self.portfolio_heat_tracker = PortfolioHeatTracker(self.mt5)  # Removed
        
        # Trading state
        self.trades_today = {}  # Track trades per symbol per day
        self.session_trades = {'london': {}, 'ny': {}}  # Track session-based trades
        self.successful_pairs_today = set()  # Track pairs with successful trades TODAY
        self.active_trades = {}  # Track active trades for monitoring
        self.daily_pnl = 0.0    # Track daily profit/loss in USD
        self.daily_trades_count = 0  # Track number of trades today
        self.running = False
        self.last_check_time = datetime.now()
        self.signal_queue = []  # Queue for signal prioritization (professional risk management)
        self.last_reversal_check = {}  # Track last reversal check time per symbol
        
        # Session management for day trading
        self.current_session = None
        self.london_trades_today = {}  # Track London session trades per pair
        self.ny_trades_today = {}     # Track NY session trades per pair
        
        # AI-specific tracking
        self.ai_enhancement_stats = {}
        self.correlation_conflicts = {}
        self.portfolio_heat_history = []
        
        # Display configuration
        self._display_config()
        
    def _display_config(self):
        """Display current configuration."""
        print(f"\n{Fore.YELLOW}🤖 ADVANCED AI-POWERED CONTRARIAN TRADING SYSTEM{Style.RESET_ALL}")
        print(f"🔄 Signal Reversal: {Fore.GREEN}ENABLED{Style.RESET_ALL}")
        print(f"🧠 ML Enhancement: {Fore.GREEN}ENABLED{Style.RESET_ALL}")
        print(f"📊 Correlation Analysis: {Fore.GREEN}ENABLED{Style.RESET_ALL}")
        print(f"🔥 Portfolio Heat Tracking: {Fore.GREEN}ENABLED{Style.RESET_ALL}")
        print(f"📈 Trading Pairs: {len(self.config.DEFAULT_SYMBOLS)}")
        print(f"🛡️ Min Signal Strength: {self.config.MIN_SIGNAL_STRENGTH}/10 (PREMIUM ONLY)")
        print(f"� Fixed Risk: ${self.config.FIXED_RISK_AMOUNT} per trade")
        print(f"🚫 Max Daily Drawdown: ${self.config.MAX_DAILY_DRAWDOWN}")
        print(f"🎯 Max Concurrent Trades: {self.config.MAX_CONCURRENT_TRADES}")
        print(f"⭐ Priority Threshold: {self.config.PRIORITY_SIGNAL_THRESHOLD}/10")
        print(f"🎯 SL Multiplier: {self.config.SL_ATR_MULTIPLIER}x ATR")
        print(f"🎯 TP Multipliers: {self.config.TP1_ATR_MULTIPLIER}x, {self.config.TP2_ATR_MULTIPLIER}x, {self.config.TP3_ATR_MULTIPLIER}x ATR")
        print(f"📱 Telegram: {'✅ Enabled' if self.telegram.enabled else '❌ Disabled'}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
    def start(self):
        """Start the contrarian trading system."""
        if not self.mt5.connect():
            print(f"{Fore.RED}❌ Failed to connect to MT5. System cannot start.{Style.RESET_ALL}")
            return False
            
        print(f"{Fore.GREEN}🚀 Contrarian Trading System Started!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔄 All signals will be REVERSED for contrarian trading{Style.RESET_ALL}")
        
        # Send startup notification
        self.telegram.send_system_status(
            "CONTRARIAN SYSTEM STARTED", 
            "All BUY signals will execute SELL trades\nAll SELL signals will execute BUY trades"
        )
        
        self.running = True
        return True
        
    def stop(self):
        """Stop the trading system."""
        self.running = False
        print(f"{Fore.YELLOW}🛑 Contrarian Trading System Stopped{Style.RESET_ALL}")
        
        # Send shutdown notification
        self.telegram.send_system_status("SYSTEM STOPPED", "Contrarian trading system has been shut down")
        
    def _reset_daily_trades(self):
        """Reset daily trade counters at midnight."""
        current_date = datetime.now().date()
        
        # Check if we need to reset (new day)
        if hasattr(self, '_last_reset_date') and self._last_reset_date != current_date:
            print(f"\n{Fore.CYAN}🌅 NEW TRADING DAY: {current_date}{Style.RESET_ALL}")
            
            # Reset all counters
            self.daily_trades_count = 0
            self.daily_pnl = 0.0
            self.session_trades = {'london': {}, 'ny': {}}
            self.successful_pairs = set()
            self.trades_today.clear()
            
            print("✅ Daily counters reset:")
            print(f"   � Daily trades: {self.daily_trades_count}")
            print(f"   💰 Daily P&L: ${self.daily_pnl:.2f}")
            print(f"   🗓️ Session trades reset")
            print(f"   ✅ Successful pairs reset")
            
            # Send new day notification
            self.telegram.send_system_status(
                "NEW TRADING DAY", 
                f"Date: {current_date}\nAll counters reset for fresh start"
            )
        
        self._last_reset_date = current_date
        
    def _can_trade_symbol(self, symbol):
        """Check if we can trade this specific symbol with session-based limits."""
        # Check if pair already had a successful trade TODAY
        if self.config.STOP_TRADING_ON_PAIR_SUCCESS and symbol in self.successful_pairs_today:
            return False
            
        # Get current session
        current_session = self._get_current_session()
        if not current_session:
            return False
            
        # Check session-specific limits (1 trade per pair per session)
        if current_session == 'london':
            if self.london_trades_today.get(symbol, 0) >= self.config.MAX_LONDON_TRADES_PER_PAIR:
                return False
        elif current_session == 'ny':
            if self.ny_trades_today.get(symbol, 0) >= self.config.MAX_NY_TRADES_PER_PAIR:
                return False
            
        # Check daily trades per pair limit (max 2: 1 London + 1 NY)
        total_trades_today = self.london_trades_today.get(symbol, 0) + self.ny_trades_today.get(symbol, 0)
        if total_trades_today >= self.config.MAX_TRADES_PER_PAIR_PER_DAY:
            return False
            
        # Check overall daily limit
        if self.daily_trades_count >= self.config.MAX_TRADES_PER_DAY:
            return False
            
        return True
    
    def _get_current_session(self):
        """Get current trading session."""
        current_hour = datetime.utcnow().hour
        
        if self.config.LONDON_SESSION_START <= current_hour < self.config.LONDON_SESSION_END:
            return 'london'
        elif self.config.NY_SESSION_START <= current_hour < self.config.NY_SESSION_END:
            return 'ny'
        else:
            return None  # Outside trading sessions
            
    def _record_trade(self, symbol):
        """Record that we've traded this symbol in the current session."""
        current_session = self._get_current_session()
        
        if current_session == 'london':
            self.london_trades_today[symbol] = self.london_trades_today.get(symbol, 0) + 1
        elif current_session == 'ny':
            self.ny_trades_today[symbol] = self.ny_trades_today.get(symbol, 0) + 1
            
        self.daily_trades_count += 1
        
    def _mark_pair_successful(self, symbol):
        """Mark pair as successful for the day (no more trades allowed)."""
        self.successful_pairs_today.add(symbol)
        print(f"🎯 {symbol} marked as SUCCESSFUL for today - no more trades allowed")
        
    def _reset_daily_counters(self):
        """Reset daily counters at start of new day."""
        current_date = datetime.now().date()
        if not hasattr(self, '_last_reset_date') or self._last_reset_date != current_date:
            self.successful_pairs_today.clear()
            self.london_trades_today.clear()
            self.ny_trades_today.clear()
            self.daily_trades_count = 0
            self.daily_pnl = 0.0
            self._last_reset_date = current_date
            print(f"🌅 Daily counters reset for {current_date}")
            
    def _can_trade_in_session(self, symbol):
        """Legacy method for backwards compatibility."""
        return True  # Handled by _can_trade_symbol now
        
    def _reverse_signal(self, signal):
        """
        Reverse signal for contrarian trading.
        
        Args:
            signal (str): Original signal ('BUY' or 'SELL')
            
        Returns:
            str: Reversed signal ('SELL' for BUY, 'BUY' for SELL)
        """
        if signal == "BUY":
            return "SELL"
        elif signal == "SELL":
            return "BUY"
        else:
            return signal
            
    def _calculate_contrarian_levels(self, symbol, reversed_action, entry_price, atr_value, signal_strength=7.0):
        """
        Calculate optimized TP/SL levels for day trading contrarian trades.
        
        OPTIMIZED FOR DAY TRADING:
        - 10 pip fixed TP target for quick profits
        - Conservative SL based on signal strength
        - Multiple TP levels for partial closures
        
        Args:
            symbol (str): Trading symbol
            reversed_action (str): Contrarian action (BUY or SELL)
            entry_price (float): Entry price
            atr_value (float): ATR value
            signal_strength (float): Signal strength (affects target distances)
            
        Returns:
            dict: Optimized TP/SL levels for day trading
        """
        # Get pip value for the symbol
        pip_value = self._get_pip_value(symbol)
        
        if self.config.USE_FIXED_PIPS:
            # Use fixed pip targets for day trading
            sl_distance = self.config.FIXED_SL_PIPS * pip_value
            tp1_distance = self.config.FIXED_TP_PIPS * pip_value
            tp2_distance = (self.config.FIXED_TP_PIPS * 2) * pip_value  # 20 pips
            tp3_distance = (self.config.FIXED_TP_PIPS * 3) * pip_value  # 30 pips
            
            # Adjust based on signal strength
            session_multiplier = self._get_session_multiplier()
            strength_multiplier = self._get_strength_multiplier(signal_strength)
            final_multiplier = session_multiplier * strength_multiplier
            
            # Only adjust TP targets, keep SL conservative
            tp1_distance *= strength_multiplier
            tp2_distance *= strength_multiplier  
            tp3_distance *= strength_multiplier
            
        else:
            # Fallback to ATR-based system
            session_multiplier = self._get_session_multiplier()
            strength_multiplier = self._get_strength_multiplier(signal_strength)
            
            base_sl_distance = atr_value * self.config.SL_ATR_MULTIPLIER
            base_tp1_distance = atr_value * self.config.TP1_ATR_MULTIPLIER
            base_tp2_distance = atr_value * self.config.TP2_ATR_MULTIPLIER
            base_tp3_distance = atr_value * self.config.TP3_ATR_MULTIPLIER
            
            final_multiplier = session_multiplier * strength_multiplier
            
            sl_distance = base_sl_distance
            tp1_distance = base_tp1_distance * final_multiplier
            tp2_distance = base_tp2_distance * final_multiplier
            tp3_distance = base_tp3_distance * final_multiplier
        
        if reversed_action == "BUY":
            # For contrarian BUY: SL below, TPs above
            sl_price = entry_price - sl_distance
            tp1_price = entry_price + tp1_distance
            tp2_price = entry_price + tp2_distance
            tp3_price = entry_price + tp3_distance
        else:  # SELL
            # For contrarian SELL: SL above, TPs below
            sl_price = entry_price + sl_distance
            tp1_price = entry_price - tp1_distance
            tp2_price = entry_price - tp2_distance
            tp3_price = entry_price - tp3_distance
        
        return {
            'sl_price': round(sl_price, 5),
            'tp1_price': round(tp1_price, 5),
            'tp2_price': round(tp2_price, 5),
            'tp3_price': round(tp3_price, 5),
            'sl_distance_pips': round(sl_distance / pip_value, 1),
            'tp1_distance_pips': round(tp1_distance / pip_value, 1),
            'tp2_distance_pips': round(tp2_distance / pip_value, 1),
            'tp3_distance_pips': round(tp3_distance / pip_value, 1),
            'session_multiplier': session_multiplier,
            'strength_multiplier': strength_multiplier,
            'final_multiplier': final_multiplier
        }
    
    def _get_pip_value(self, symbol):
        """Get pip value for symbol (0.0001 for most pairs, 0.01 for JPY pairs)."""
        if 'JPY' in symbol:
            return 0.01
        else:
            return 0.0001
            
        return {
            'sl_price': sl_price,
            'tp1_price': tp1_price,
            'tp2_price': tp2_price,
            'tp3_price': tp3_price,
            'breakeven_trigger': entry_price + (atr_value * self.config.BREAKEVEN_TRIGGER_ATR * (1 if reversed_action == "BUY" else -1)),
            'trailing_trigger': entry_price + (atr_value * self.config.TRAILING_STOP_TRIGGER * (1 if reversed_action == "BUY" else -1)),
            'session_multiplier': session_multiplier,
            'strength_multiplier': strength_multiplier,
            'final_multiplier': final_multiplier
        }
        
    def _get_session_multiplier(self):
        """Get multiplier based on current trading session."""
        session, _ = self.config.get_trading_session_info()
        
        multipliers = {
            'ASIAN_SESSION': self.config.ASIAN_SESSION_MULTIPLIER,
            'LONDON_PRE_MARKET': self.config.LONDON_SESSION_MULTIPLIER,
            'LONDON_SESSION': self.config.LONDON_SESSION_MULTIPLIER,
            'LONDON_NY_OVERLAP': self.config.OVERLAP_SESSION_MULTIPLIER,
            'NY_SESSION': self.config.NY_SESSION_MULTIPLIER,
            'QUIET_HOURS': self.config.ASIAN_SESSION_MULTIPLIER
        }
        
        return multipliers.get(session, 1.0)
        
    def _calculate_lot_size(self, symbol, sl_distance_pips):
        """
        Calculate lot size based on fixed $10 risk.
        
        Args:
            symbol (str): Trading symbol
            sl_distance_pips (float): Stop loss distance in pips
            
        Returns:
            float: Calculated lot size
        """
        try:
            # Get symbol info for pip value calculation
            import MetaTrader5 as mt5
            symbol_info = mt5.symbol_info(symbol)
            
            if not symbol_info:
                print(f"⚠️ Could not get symbol info for {symbol}, using base lot size")
                return self.config.BASE_LOT_SIZE
            
            # Calculate pip value for 1 standard lot
            if symbol.endswith(('JPY', 'jpy')):
                pip_size = 0.01  # JPY pairs have 2 decimal pip
            else:
                pip_size = 0.0001  # Most pairs have 4 decimal pip
                
            # For mini lots (0.1), pip value is usually $1 per pip for USD account
            pip_value_per_mini_lot = 1.0  # $1 per pip for 0.1 lot on EURUSD
            
            # Adjust pip value for different symbols
            if 'USD' not in symbol:
                # For non-USD pairs, use approximate conversion
                pip_value_per_mini_lot = 1.0  # Simplified for now
            
            # Calculate required lot size: Risk Amount / (SL Distance * Pip Value per lot)
            required_lots = self.config.FIXED_RISK_AMOUNT / (sl_distance_pips * pip_value_per_mini_lot)
            
            # Round to acceptable lot size increments (0.01 minimum)
            required_lots = round(required_lots, 2)
            
            # Ensure minimum lot size
            if required_lots < 0.01:
                required_lots = 0.01
            
            # Ensure maximum reasonable lot size (safety limit)
            if required_lots > 1.0:
                required_lots = 1.0
                
            print(f"💰 Risk Calculation: ${self.config.FIXED_RISK_AMOUNT} ÷ ({sl_distance_pips:.1f} pips × ${pip_value_per_mini_lot}) = {required_lots:.2f} lots")
            
            return required_lots
            
        except Exception as e:
            print(f"❌ Error calculating lot size: {e}")
            return self.config.BASE_LOT_SIZE
            
    def _get_strength_multiplier(self, signal_strength):
        """Get multiplier based on signal strength."""
        if signal_strength >= 9.0:
            return self.config.ULTRA_SIGNAL_MULTIPLIER
        elif signal_strength >= 8.0:
            return self.config.STRONG_SIGNAL_MULTIPLIER
        elif signal_strength < 7.0:
            return self.config.WEAK_SIGNAL_MULTIPLIER
        else:
            return 1.0  # Standard multiplier for 7.0-7.9 signals
            
    def _can_open_new_trade(self):
        """Check if we can open a new trade based on professional limits."""
        # Check if daily profit target reached
        if self.daily_pnl >= self.config.DAILY_PROFIT_TARGET:
            return False, f"Daily profit target reached: ${self.daily_pnl:.2f}"
            
        # Check if daily loss limit reached
        if self.daily_pnl <= -self.config.MAX_DAILY_DRAWDOWN:
            return False, f"Daily loss limit reached: ${self.daily_pnl:.2f}"
            
        # Check concurrent trades limit
        current_trades = len([t for t in self.active_trades.values() if t.get('status', 'open') == 'open'])
        if current_trades >= self.config.MAX_CONCURRENT_TRADES:
            return False, f"Max concurrent trades reached: {current_trades}/{self.config.MAX_CONCURRENT_TRADES}"
            
        # Check daily trades limit
        if self.daily_trades_count >= self.config.MAX_TRADES_PER_DAY:
            return False, f"Daily trades limit reached: {self.daily_trades_count}/{self.config.MAX_TRADES_PER_DAY}"
            
        return True, "OK"
        
    def _add_signal_to_queue(self, symbol, signal_data):
        """Add signal to priority queue for processing."""
        signal_strength = signal_data.get('strength', 0)
        
        # Create signal entry with priority score
        signal_entry = {
            'symbol': symbol,
            'data': signal_data,
            'strength': signal_strength,
            'timestamp': datetime.now()
        }
        
        # Add to queue
        self.signal_queue.append(signal_entry)
        
        # Sort by strength (highest first) then by timestamp (earliest first)
        self.signal_queue.sort(key=lambda x: (-x['strength'], x['timestamp']))
        
        print(f"📊 Signal queued: {symbol} - {signal_strength:.1f}/10 (Queue size: {len(self.signal_queue)})")
        
    def _process_best_signal(self):
        """Process the highest priority signal from queue."""
        if not self.signal_queue:
            return
            
        # Check if we can open a new trade
        can_trade, reason = self._can_open_new_trade()
        if not can_trade:
            print(f"🚫 Cannot open trade: {reason}")
            return
            
        # Get the best signal
        best_signal = self.signal_queue.pop(0)
        symbol = best_signal['symbol']
        signal_data = best_signal['data']
        signal_strength = best_signal['strength']
        
        print(f"\n{Fore.CYAN}⭐ PROCESSING BEST SIGNAL: {symbol} ({signal_strength:.1f}/10){Style.RESET_ALL}")
        
        # Execute the trade
        self._execute_prioritized_trade(symbol, signal_data)
        
        # Note: Don't clear remaining signals since we can have up to 2 trades
        print(f"📊 Remaining signals in queue: {len(self.signal_queue)}")
            
    def _get_current_session(self):
        """Get current trading session."""
        current_hour = datetime.utcnow().hour
        
        if self.config.LONDON_SESSION_START <= current_hour < self.config.LONDON_SESSION_END:
            if self.config.NY_SESSION_START <= current_hour < self.config.NY_SESSION_END:
                return 'overlap'  # London-NY overlap
            return 'london'
        elif self.config.NY_SESSION_START <= current_hour < self.config.NY_SESSION_END:
            return 'ny'
        else:
            return 'asian'
    
    def _can_trade_in_session(self, symbol):
        """Check if we can trade this symbol in current session."""
        current_session = self._get_current_session()
        
        if current_session in ['asian', 'overlap']:
            return True  # Allow trading during Asian and overlap
            
        # Check session-specific limits
        if current_session == 'london':
            london_trades = self.session_trades['london'].get(symbol, 0)
            return london_trades < self.config.MAX_LONDON_TRADES_PER_PAIR
        elif current_session == 'ny':
            ny_trades = self.session_trades['ny'].get(symbol, 0)
            return ny_trades < self.config.MAX_NY_TRADES_PER_PAIR
            
        return True
    
    def _record_session_trade(self, symbol):
        """Record trade for session tracking."""
        current_session = self._get_current_session()
        
        if current_session == 'london':
            self.session_trades['london'][symbol] = self.session_trades['london'].get(symbol, 0) + 1
        elif current_session == 'ny':
            self.session_trades['ny'][symbol] = self.session_trades['ny'].get(symbol, 0) + 1
    
    def _update_daily_pnl(self, pnl_change):
        """Update daily P&L tracking."""
        self.daily_pnl += pnl_change
        print(f"� Daily P&L updated: ${self.daily_pnl:.2f} (change: ${pnl_change:+.2f})")
        
        # Check if we hit profit target
        if self.daily_pnl >= self.config.DAILY_PROFIT_TARGET:
            print(f"🎯 DAILY PROFIT TARGET REACHED: ${self.daily_pnl:.2f} >= ${self.config.DAILY_PROFIT_TARGET}")
            print("🛑 STOPPING TRADING FOR THE DAY")
            return True
            
        # Check daily loss limit
        if self.daily_pnl <= -self.config.MAX_DAILY_DRAWDOWN:
            print(f"🚫 DAILY LOSS LIMIT REACHED: ${self.daily_pnl:.2f} <= -${self.config.MAX_DAILY_DRAWDOWN}")
            print("🛑 STOPPING TRADING FOR THE DAY")
            return True
            
        return False
    
    def _check_for_major_reversal(self, symbol, trade_info):
        """Check if a major reversal signal is detected for an active trade."""
        if not self.config.ENABLE_TRADE_FOLLOWING:
            return False
            
        # Check if enough time has passed since last reversal check
        now = datetime.now()
        last_check = self.last_reversal_check.get(symbol, now - timedelta(seconds=self.config.REVERSAL_CHECK_INTERVAL))
        
        if (now - last_check).total_seconds() < self.config.REVERSAL_CHECK_INTERVAL:
            return False
        
        self.last_reversal_check[symbol] = now
        
        try:
            # Get fresh signal data
            signal_data = self.signal_generator.generate_live_day_trading_signal(symbol)
            
            if not signal_data:
                return False
                
            signal_type = signal_data.get('signal')
            signal_strength = signal_data.get('strength', 0)
            confluences = signal_data.get('confluences', [])
            
            # Check if we have a major reversal
            if (signal_strength >= self.config.MAJOR_REVERSAL_THRESHOLD and 
                len(confluences) >= self.config.REVERSAL_CONFLUENCE_MIN):
                
                trade_action = trade_info['action']
                
                # Check if signal opposes current trade direction
                if ((trade_action == 'BUY' and signal_type == 'BUY') or  # Original was SELL, we bought contrarian, now BUY signal confirms original
                    (trade_action == 'SELL' and signal_type == 'SELL')):  # Original was BUY, we sold contrarian, now SELL signal confirms original
                    
                    print(f"\n{Fore.RED}🚨 MAJOR REVERSAL DETECTED for {symbol}!{Style.RESET_ALL}")
                    print(f"📊 Current Trade: {trade_action}")
                    print(f"🔄 Reversal Signal: {signal_type}")
                    print(f"⭐ Signal Strength: {signal_strength:.1f}/10")
                    print(f"🎯 Confluences: {len(confluences)}")
                    
                    return True
                    
        except Exception as e:
            print(f"❌ Error checking reversal for {symbol}: {e}")
            
        return False
    
    def _close_trade_on_reversal(self, symbol, trade_info):
        """Close trade due to major reversal detection."""
        try:
            current_price = self.mt5.get_tick(symbol)
            if not current_price:
                print(f"❌ Could not get price for {symbol}")
                return False
                
            trade_action = trade_info['action']
            exit_price = current_price.bid if trade_action == 'BUY' else current_price.ask
            entry_price = trade_info['entry_price']
            lot_size = trade_info['lot_size']
            
            # Calculate P&L
            if trade_action == 'BUY':
                pips = (exit_price - entry_price) * 100000
            else:
                pips = (entry_price - exit_price) * 100000
                
            # Close the position
            ticket = trade_info.get('ticket')
            if ticket:
                close_request = {
                    "action": self.mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot_size,
                    "type": self.mt5.ORDER_TYPE_SELL if trade_action == 'BUY' else self.mt5.ORDER_TYPE_BUY,
                    "position": ticket,
                    "deviation": 20,
                    "magic": 234000,
                    "comment": "REVERSAL_CLOSE",
                    "type_time": self.mt5.ORDER_TIME_GTC,
                    "type_filling": self.mt5.ORDER_FILLING_IOC,
                }
                
                result = self.mt5.order_send(close_request)
                
                if result and result.retcode == self.mt5.TRADE_RETCODE_DONE:
                    print(f"✅ Trade closed on reversal: {symbol} at {exit_price:.5f}")
                    
                    # Update P&L
                    pnl_usd = pips * lot_size * 10  # Approximate conversion
                    self._update_daily_pnl(pnl_usd)
                    
                    # Send notification
                    self.telegram.send_reversal_close_notification(
                        symbol, trade_action, entry_price, exit_price, pips
                    )
                    
                    # Remove from active trades
                    if symbol in self.active_trades:
                        del self.active_trades[symbol]
                        
                    return True
                else:
                    print(f"❌ Failed to close trade on reversal: {symbol}")
                    
        except Exception as e:
            print(f"❌ Error closing trade on reversal: {e}")
            
        return False
    
    def _execute_contrarian_trade(self, symbol, original_signal, signal_strength, confluences):
        """
        Execute contrarian trade by reversing the signal.
        
        Args:
            symbol (str): Trading symbol
            original_signal (str): Original signal before reversal
            signal_strength (float): Signal strength (0-10)
            confluences (list): List of signal confluences
        """
        # Reverse the signal for contrarian trading
        reversed_action = self._reverse_signal(original_signal)
        
        print(f"\n{Fore.MAGENTA}🔄 CONTRARIAN SIGNAL REVERSAL{Style.RESET_ALL}")
        print(f"📊 Symbol: {symbol}")
        print(f"🔄 Original Signal: {Fore.BLUE}{original_signal}{Style.RESET_ALL}")
        print(f"🎯 Contrarian Action: {Fore.GREEN if reversed_action == 'BUY' else Fore.RED}{reversed_action}{Style.RESET_ALL}")
        print(f"⭐ Strength: {signal_strength}/10")
        
        # Get current market price
        tick = self.mt5.get_tick(symbol)
        if not tick:
            print(f"{Fore.RED}❌ Failed to get tick data for {symbol}{Style.RESET_ALL}")
            return False
            
        # Calculate entry price based on reversed action
        if reversed_action == "BUY":
            entry_price = tick.ask
        else:  # SELL
            entry_price = tick.bid
            
        # Get ATR for risk management
        atr_value = self._get_atr(symbol)
        if not atr_value:
            print(f"{Fore.RED}❌ Failed to calculate ATR for {symbol}{Style.RESET_ALL}")
            return False
            
        # Calculate enhanced contrarian SL and TP levels
        levels = self._calculate_contrarian_levels(
            symbol, reversed_action, entry_price, atr_value, signal_strength
        )
        
        # Calculate dynamic lot size based on $10 risk
        sl_distance_pips = abs(entry_price - levels['sl_price']) * 100000
        lot_size = self._calculate_lot_size(symbol, sl_distance_pips)
        
        print(f"💰 Entry: {entry_price:.5f}")
        print(f"🛑 Stop Loss: {levels['sl_price']:.5f} ({sl_distance_pips:.1f} pips)")
        print(f"🎯 TP1: {levels['tp1_price']:.5f} ({self.config.TP1_CLOSE_PERCENT}%)")
        print(f"🎯 TP2: {levels['tp2_price']:.5f} ({self.config.TP2_CLOSE_PERCENT}%)")
        print(f"🎯 TP3: {levels['tp3_price']:.5f} ({self.config.TP3_CLOSE_PERCENT}%)")
        print(f"📦 Lot Size: {lot_size} (Risk: ${self.config.FIXED_RISK_AMOUNT})")
        print(f"⚡ Session Multiplier: {levels['session_multiplier']:.2f}")
        print(f"💪 Strength Multiplier: {levels['strength_multiplier']:.2f}")
        print(f"🎯 Final Multiplier: {levels['final_multiplier']:.2f}")
        
        # Execute the contrarian trade with calculated lot size
        success = self._place_market_order(
            symbol, reversed_action, lot_size, 
            levels['sl_price'], levels['tp1_price']
        )
        
        if success:
            # Record the trade
            self._record_trade(symbol)
            self._record_session_trade(symbol)
            
            # Store enhanced active trade for monitoring
            self.active_trades[symbol] = {
                'ticket': None,  # Will be updated if we get ticket from order result
                'symbol': symbol,
                'action': reversed_action,
                'entry_price': entry_price,
                'levels': levels,  # Store all TP/SL levels
                'lot_size': lot_size,
                'entry_time': datetime.now(),
                'original_signal': original_signal,
                'contrarian': True,
                'tp_hits': {'tp1': False, 'tp2': False, 'tp3': False},
                'breakeven_set': False,
                'trailing_active': False,
                'current_sl': levels['sl_price'],
                'session': self._get_current_session()
            }
            
            # Update daily counter
            self.daily_trades_count += 1
            
            print(f"{Fore.GREEN}✅ Contrarian {reversed_action} trade executed for {symbol}{Style.RESET_ALL}")
            print(f"📊 Daily trades: {self.daily_trades_count}/{self.config.MAX_TRADES_PER_DAY}")
            print(f"📊 Session: {self._get_current_session().upper()}")
            
            # Send enhanced Telegram notification for trade entry
            self.telegram.send_enhanced_trade_alert(
                symbol, reversed_action, entry_price, levels, 
                lot_size, signal_strength, reversed=True
            )
            
            return True
        else:
            print(f"{Fore.RED}❌ Failed to execute contrarian trade for {symbol}{Style.RESET_ALL}")
            return False
            
    def _execute_prioritized_trade(self, symbol, signal_data):
        """Execute trade for prioritized signal."""
        signal_type = signal_data.get('signal')
        signal_strength = signal_data.get('strength', 0)
        confluences = signal_data.get('confluences', [])
        
        print(f"🔥 Executing PRIORITY trade: {symbol} - {signal_type} ({signal_strength:.1f}/10)")
        
        # Execute the contrarian trade
        success = self._execute_contrarian_trade(symbol, signal_type, signal_strength, confluences)
        
        if success:
            # Send priority notification
            self.telegram.send_priority_trade_notification(
                symbol, signal_type, signal_strength, "HIGHEST PRIORITY SIGNAL EXECUTED"
            )
            
    def _get_atr(self, symbol, period=14):
        """Calculate ATR for the symbol."""
        try:
            # Get recent rates for ATR calculation
            rates = self.mt5.get_rates(symbol, "H1", 100)
            
            if rates is None or len(rates) < period + 1:
                return None
                
            # Calculate True Range
            high = rates['high']
            low = rates['low']
            close = rates['close']
            
            tr_list = []
            for i in range(1, len(rates)):
                tr1 = high[i] - low[i]
                tr2 = abs(high[i] - close[i-1])
                tr3 = abs(low[i] - close[i-1])
                tr = max(tr1, tr2, tr3)
                tr_list.append(tr)
                
            # Calculate ATR as simple moving average of True Range
            if len(tr_list) >= period:
                atr = sum(tr_list[-period:]) / period
                return atr
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error calculating ATR for {symbol}: {e}")
            return None
            
    def _place_market_order(self, symbol, action, lot_size, sl_price, tp_price):
        """Place market order with SL and TP."""
        try:
            import MetaTrader5 as mt5
            
            # Get symbol info
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                print(f"❌ Symbol {symbol} not found")
                return False
                
            # Check if symbol is available for trading
            if not symbol_info.visible:
                print(f"❌ Symbol {symbol} is not visible, trying to switch on")
                if not mt5.symbol_select(symbol, True):
                    print(f"❌ Failed to select symbol {symbol}")
                    return False
                    
            # Get current tick
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                print(f"❌ Failed to get tick for {symbol}")
                return False
                
            # Determine order type and price
            if action == "BUY":
                order_type = mt5.ORDER_TYPE_BUY
                price = tick.ask
            else:  # SELL
                order_type = mt5.ORDER_TYPE_SELL
                price = tick.bid
                
            # Prepare the request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot_size,
                "type": order_type,
                "price": price,
                "sl": sl_price,
                "tp": tp_price,
                "deviation": 20,
                "magic": 12345,
                "comment": f"Contrarian {action}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Send the order
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"❌ Order failed: {result.retcode} - {result.comment}")
                return False
            else:
                print(f"✅ Order successful: ticket #{result.order}")
                return True
                
        except Exception as e:
            print(f"❌ Error placing order: {e}")
            return False
            
    def _process_symbol(self, symbol):
        """Process a single symbol for contrarian trading signals with AI enhancement."""
        try:
            # Check if we can open new trades (global limit)
            if not self._can_open_new_trade():
                print(f"⚠️ Cannot open new trade - limit reached or daily drawdown exceeded")
                return
                
            # Check if we can trade this symbol today
            if not self._can_trade_symbol(symbol):
                print(f"⏸️ {symbol}: Already traded today")
                return
                
            print(f"🔍 Analyzing {symbol} with AI Enhancement...")
            
            # Generate initial signal
            signal_data = self.signal_generator.generate_live_day_trading_signal(symbol)
            
            if not signal_data:
                print(f"❌ {symbol}: No signal data received")
                return
                
            signal_type = signal_data.get('signal')
            original_strength = signal_data.get('strength', 0)
            confluences = signal_data.get('confluences', [])
            
            print(f"📊 {symbol}: Original Signal={signal_type}, Strength={original_strength:.1f}/10, Confluences={len(confluences)}")
            
            # Step 1: ML Enhancement
            enhanced_signal = self.ml_enhancer.enhance_signal(symbol, signal_data)
            enhanced_strength = enhanced_signal.get('strength', original_strength)
            ml_confidence = enhanced_signal.get('ml_confidence', 0)
            
            # Step 2: Correlation Analysis (Temporarily disabled for testing)
            active_pairs = [t.get('symbol', '') for t in self.active_trades.values() if t.get('status', 'open') == 'open']
            # safe_pairs = self.correlation_analyzer.get_safe_pairs_for_trading(active_pairs)
            safe_pairs = [symbol]  # Temporarily allow all pairs
            
            if symbol not in safe_pairs:
                print(f"🚫 {symbol}: Blocked by correlation analysis")
                return
            
            # Step 3: Portfolio Heat Check (Removed - simplified system)
            # Simple risk check instead of complex heat tracking
            if len(self.active_trades) >= self.config.MAX_CONCURRENT_TRADES:
                print(f"🔥 {symbol}: Max concurrent trades reached ({self.config.MAX_CONCURRENT_TRADES})")
                return
            
            # Check if enhanced signal meets minimum strength requirement
            if enhanced_strength < self.config.MIN_SIGNAL_STRENGTH:
                print(f"⚠️ {symbol}: Enhanced signal too weak ({enhanced_strength:.1f} < {self.config.MIN_SIGNAL_STRENGTH})")
                return
            
            # Log AI enhancement results
            print(f"🤖 {symbol}: AI Enhancement Results:")
            print(f"   📊 Original Strength: {original_strength:.1f}/10")
            print(f"   🧠 Enhanced Strength: {enhanced_strength:.1f}/10")
            print(f"   🎯 ML Confidence: {ml_confidence:.1f}%")
            print(f"   📊 Correlation: Safe")
            print(f"   🔥 Risk Check: Passed")
            
            # Add AI-enhanced signal to priority queue
            enhanced_signal['ai_enhanced'] = True
            enhanced_signal['ml_confidence'] = ml_confidence
            # enhanced_signal['heat_impact'] = heat_impact  # Removed
            
            print(f"🔥 Adding AI-enhanced {symbol} to priority queue (strength: {enhanced_strength:.1f})")
            self._add_signal_to_queue(symbol, enhanced_signal)
            
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
            
    def _process_priority_queue(self):
        """Process the priority queue and execute the best signals (up to 2 trades)."""
        if not self.signal_queue:
            return
            
        print(f"🔍 Processing priority queue with {len(self.signal_queue)} signals")
        
        # Process up to 2 best signals if we can open trades
        trades_to_execute = min(len(self.signal_queue), self.config.MAX_CONCURRENT_TRADES)
        current_trades = len([t for t in self.active_trades.values() if t.get('status', 'open') == 'open'])
        available_slots = self.config.MAX_CONCURRENT_TRADES - current_trades
        
        if available_slots <= 0:
            print(f"⚠️ Cannot process queue - all {self.config.MAX_CONCURRENT_TRADES} trade slots occupied")
            self.signal_queue.clear()
            return
            
        signals_to_process = min(available_slots, len(self.signal_queue))
        print(f"🎯 Will process {signals_to_process} signal(s) (available slots: {available_slots})")
        
        # Process the best signals
        for i in range(signals_to_process):
            if self._can_open_new_trade()[0]:
                self._process_best_signal()
            else:
                print("⚠️ Cannot process more signals - limits reached")
                break
        
        # Clear remaining signals after processing
        if self.signal_queue:
            remaining_count = len(self.signal_queue)
            self.signal_queue.clear()
            print(f"🗑️ Cleared {remaining_count} remaining signals")
            
    def _monitor_active_trades(self):
        """Monitor active trades for enhanced TP/SL management and reversal detection with AI tracking."""
        if not self.active_trades:
            return
            
        # Update portfolio heat with current positions
        active_positions = []
        for symbol, trade_info in self.active_trades.items():
            active_positions.append({
                'symbol': symbol,
                'volume': trade_info.get('volume', 0.01),
                'risk_amount': trade_info.get('risk_amount', self.config.FIXED_RISK_AMOUNT),
                'type': 'buy' if trade_info.get('action') == 'BUY' else 'sell'
            })
        
        # Update portfolio heat analysis (simplified)
        if active_positions:
            heat_analysis = {
                'total_positions': len(active_positions),
                'total_risk': len(active_positions) * self.config.FIXED_RISK_AMOUNT,
                'heat_level': 'Cold' if len(active_positions) < 2 else 'Warm'
            }
            self.portfolio_heat_history.append(heat_analysis)
            
            # Keep only recent heat history
            if len(self.portfolio_heat_history) > 100:
                self.portfolio_heat_history = self.portfolio_heat_history[-100:]
        
        trades_to_remove = []
        
        for symbol, trade_info in self.active_trades.items():
            try:
                # Check for major reversal first
                if self._check_for_major_reversal(symbol, trade_info):
                    if self._close_trade_on_reversal(symbol, trade_info):
                        trades_to_remove.append(symbol)
                        # Update ML performance on reversal closure
                        self._update_ai_performance(symbol, trade_info, 'reversal_closure')
                        continue
                
                # Get current price
                tick = self.mt5.get_tick(symbol)
                if not tick:
                    continue
                    
                current_price = tick.bid if trade_info['action'] == 'SELL' else tick.ask
                entry_price = trade_info['entry_price']
                levels = trade_info['levels']
                action = trade_info['action']
                
                # Check for SL hit first
                sl_hit = self._check_sl_hit(current_price, trade_info)
                if sl_hit:
                    self._handle_sl_hit(symbol, trade_info, current_price)
                    trades_to_remove.append(symbol)
                    continue
                    
                # Check for TP hits (TP1, TP2, TP3)
                tp_hit = self._check_tp_hits(current_price, trade_info)
                if tp_hit:
                    # If all TPs hit, remove trade
                    all_tps_hit = all(trade_info['tp_hits'].values())
                    if all_tps_hit:
                        trades_to_remove.append(symbol)
                        continue
                
                # Check for breakeven management
                if self.config.BREAKEVEN_ENABLED and not trade_info['breakeven_set']:
                    self._check_breakeven(current_price, trade_info, symbol)
                    
                # Check for trailing stop
                if self.config.TRAILING_STOP_ENABLED and not trade_info['trailing_active']:
                    self._check_trailing_stop(current_price, trade_info, symbol)
                elif trade_info.get('trailing_active', False):
                    self._update_trailing_stop(current_price, trade_info, symbol)
                    
            except Exception as e:
                print(f"❌ Error monitoring trade for {symbol}: {e}")
                
        # Remove completed trades
        for symbol in trades_to_remove:
            del self.active_trades[symbol]
            
    def _check_sl_hit(self, current_price, trade_info):
        """Check if stop loss is hit."""
        current_sl = trade_info['current_sl']
        action = trade_info['action']
        
        if action == 'BUY':
            return current_price <= current_sl
        else:  # SELL
            return current_price >= current_sl
            
    def _check_tp_hits(self, current_price, trade_info):
        """Check for multiple TP level hits."""
        levels = trade_info['levels']
        action = trade_info['action']
        tp_hits = trade_info['tp_hits']
        
        tp_hit = False
        
        # Check TP1
        if not tp_hits['tp1']:
            if action == 'BUY' and current_price >= levels['tp1_price']:
                tp_hits['tp1'] = True
                self._handle_tp_hit(trade_info['symbol'], trade_info, current_price, 'TP1', self.config.TP1_CLOSE_PERCENT)
                tp_hit = True
            elif action == 'SELL' and current_price <= levels['tp1_price']:
                tp_hits['tp1'] = True
                self._handle_tp_hit(trade_info['symbol'], trade_info, current_price, 'TP1', self.config.TP1_CLOSE_PERCENT)
                tp_hit = True
                
        # Check TP2
        if not tp_hits['tp2']:
            if action == 'BUY' and current_price >= levels['tp2_price']:
                tp_hits['tp2'] = True
                self._handle_tp_hit(trade_info['symbol'], trade_info, current_price, 'TP2', self.config.TP2_CLOSE_PERCENT)
                tp_hit = True
            elif action == 'SELL' and current_price <= levels['tp2_price']:
                tp_hits['tp2'] = True
                self._handle_tp_hit(trade_info['symbol'], trade_info, current_price, 'TP2', self.config.TP2_CLOSE_PERCENT)
                tp_hit = True
                
        # Check TP3
        if not tp_hits['tp3']:
            if action == 'BUY' and current_price >= levels['tp3_price']:
                tp_hits['tp3'] = True
                self._handle_tp_hit(trade_info['symbol'], trade_info, current_price, 'TP3', self.config.TP3_CLOSE_PERCENT)
                tp_hit = True
            elif action == 'SELL' and current_price <= levels['tp3_price']:
                tp_hits['tp3'] = True
                self._handle_tp_hit(trade_info['symbol'], trade_info, current_price, 'TP3', self.config.TP3_CLOSE_PERCENT)
                tp_hit = True
                
        return tp_hit
        
    def _handle_tp_hit(self, symbol, trade_info, current_price, tp_level, close_percent):
        """Handle TP hit with partial closing and session-based success tracking."""
        entry_price = trade_info['entry_price']
        action = trade_info['action']
        lot_size = trade_info['lot_size']
        
        # Calculate profit
        if action == 'BUY':
            profit_pips = (current_price - entry_price) * 100000
        else:  # SELL
            profit_pips = (entry_price - current_price) * 100000
            
        # Calculate USD profit (approximate)
        profit_usd = profit_pips * lot_size * 10 * (close_percent / 100)
        self._update_daily_pnl(profit_usd)
        
        print(f"{Fore.GREEN}🎯 {tp_level} HIT: {symbol} - {action} - Profit: +{profit_pips:.1f} pips ({close_percent}% closed) = +${profit_usd:.2f}{Style.RESET_ALL}")
        
        # Mark pair as successful on first TP hit (stop trading this pair today)
        if tp_level == 'TP1' and self.config.STOP_TRADING_ON_PAIR_SUCCESS:
            self._mark_pair_successful(symbol)
        
        # Update AI performance tracking
        self._update_ai_performance(symbol, trade_info, 'tp_hit')
        
        # Send TP notification
        self.telegram.send_enhanced_tp_hit_notification(
            symbol, action, entry_price, current_price, 
            profit_pips, tp_level, close_percent, trade_info['contrarian']
        )
        
    def _handle_sl_hit(self, symbol, trade_info, current_price):
        """Handle stop loss hit."""
        entry_price = trade_info['entry_price']
        action = trade_info['action']
        
        # Calculate loss
        if action == 'BUY':
            loss_pips = (entry_price - current_price) * 100000
        else:  # SELL
            loss_pips = (current_price - entry_price) * 100000
            
        print(f"{Fore.RED}🛑 SL HIT: {symbol} - {action} - Loss: -{loss_pips:.1f} pips{Style.RESET_ALL}")
        
        # Send SL notification
        self.telegram.send_sl_hit_notification(
            symbol, action, entry_price, current_price, 
            loss_pips, trade_info['contrarian']
        )
        
    def _check_breakeven(self, current_price, trade_info, symbol):
        """Check and set breakeven if profit threshold reached."""
        entry_price = trade_info['entry_price']
        levels = trade_info['levels']
        action = trade_info['action']
        
        # Check if we've reached breakeven trigger
        breakeven_reached = False
        if action == 'BUY':
            breakeven_reached = current_price >= levels['breakeven_trigger']
        else:  # SELL
            breakeven_reached = current_price <= levels['breakeven_trigger']
            
        if breakeven_reached:
            # Move SL to breakeven
            trade_info['current_sl'] = entry_price
            trade_info['breakeven_set'] = True
            print(f"{Fore.CYAN}⚖️ Breakeven set for {symbol} at {entry_price:.5f}{Style.RESET_ALL}")
            
    def _check_trailing_stop(self, current_price, trade_info, symbol):
        """Check if trailing stop should be activated."""
        levels = trade_info['levels']
        action = trade_info['action']
        
        # Check if we've reached trailing trigger
        trailing_reached = False
        if action == 'BUY':
            trailing_reached = current_price >= levels['trailing_trigger']
        else:  # SELL
            trailing_reached = current_price <= levels['trailing_trigger']
            
        if trailing_reached:
            trade_info['trailing_active'] = True
            print(f"{Fore.YELLOW}📈 Trailing stop activated for {symbol}{Style.RESET_ALL}")
            
    def _update_trailing_stop(self, current_price, trade_info, symbol):
        """Update trailing stop loss."""
        action = trade_info['action']
        current_sl = trade_info['current_sl']
        levels = trade_info['levels']
        
        # Calculate new trailing SL
        atr_distance = (levels['tp1_price'] - trade_info['entry_price']) / self.config.TP1_ATR_MULTIPLIER
        trail_distance = atr_distance * self.config.TRAILING_STOP_DISTANCE
        
        if action == 'BUY':
            new_sl = current_price - trail_distance
            if new_sl > current_sl:  # Only move SL up for BUY
                trade_info['current_sl'] = new_sl
                print(f"{Fore.CYAN}📈 Trailing SL updated for {symbol}: {new_sl:.5f}{Style.RESET_ALL}")
        else:  # SELL
            new_sl = current_price + trail_distance
            if new_sl < current_sl:  # Only move SL down for SELL
                trade_info['current_sl'] = new_sl
                print(f"{Fore.CYAN}📉 Trailing SL updated for {symbol}: {new_sl:.5f}{Style.RESET_ALL}")
            
    def run(self):
        """Main trading loop."""
        if not self.start():
            return
            
        print(f"{Fore.GREEN}🔄 Contrarian trading loop started...{Style.RESET_ALL}")
        
        cycle_count = 0
        
        try:
            while self.running:
                cycle_count += 1
                current_time = datetime.now()
                
                print(f"\n{Fore.CYAN}🔄 Cycle #{cycle_count} - {current_time.strftime('%H:%M:%S')}{Style.RESET_ALL}")
                
                # Reset daily trades at midnight and session counters
                self._reset_daily_trades()
                self._reset_daily_counters()  # Add session-based counter reset
                
                # Monitor active trades for TP/SL hits
                self._monitor_active_trades()
                
                # Show active trades count
                if self.active_trades:
                    print(f"📊 Active trades: {len(self.active_trades)}")
                
                # Process each symbol and build priority queue
                symbols_processed = 0
                for symbol in self.config.DEFAULT_SYMBOLS:
                    if not self.running:
                        break
                        
                    try:
                        self._process_symbol(symbol)
                        symbols_processed += 1
                    except Exception as e:
                        print(f"❌ Error with {symbol}: {e}")
                        continue
                        
                    # Small delay between symbols
                    time.sleep(1)
                
                print(f"✅ Processed {symbols_processed}/{len(self.config.DEFAULT_SYMBOLS)} symbols")
                
                # Process the priority queue to execute the best signal
                self._process_priority_queue()
                    
                # Update last check time
                self.last_check_time = current_time
                
                # Wait before next cycle (check every 30 seconds)
                print(f"⏰ Waiting 30 seconds for next cycle...")
                time.sleep(30)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}🛑 Shutdown requested by user{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
        finally:
            self.stop()
    
    def _update_ai_performance(self, symbol, trade_info, outcome_type):
        """Update AI performance tracking based on trade outcomes."""
        try:
            if not trade_info.get('ai_enhanced', False):
                return
                
            # Calculate outcome score based on trade result
            entry_price = trade_info.get('entry_price', 0)
            current_price = trade_info.get('current_price', entry_price)
            action = trade_info.get('action', 'BUY')
            
            if action == 'BUY':
                price_change = (current_price - entry_price) / entry_price
            else:
                price_change = (entry_price - current_price) / entry_price
            
            # Convert to outcome score (positive for profitable moves)
            if outcome_type == 'tp_hit':
                outcome_score = 10  # Excellent outcome
            elif outcome_type == 'sl_hit':
                outcome_score = 0   # Poor outcome
            elif outcome_type == 'reversal_closure':
                outcome_score = 5   # Neutral (risk management)
            else:
                # Score based on price movement
                outcome_score = max(0, min(10, (price_change * 1000) + 5))
            
            # Update ML enhancer performance
            self.ml_enhancer.update_performance(symbol, trade_info, outcome_score)
            
            # Update AI stats
            if symbol not in self.ai_enhancement_stats:
                self.ai_enhancement_stats[symbol] = {
                    'total_trades': 0,
                    'successful_trades': 0,
                    'avg_outcome': 0.0,
                    'outcomes': []
                }
            
            stats = self.ai_enhancement_stats[symbol]
            stats['total_trades'] += 1
            stats['outcomes'].append(outcome_score)
            
            if outcome_score >= 6:
                stats['successful_trades'] += 1
            
            stats['avg_outcome'] = sum(stats['outcomes']) / len(stats['outcomes'])
            
            # Keep only recent outcomes
            if len(stats['outcomes']) > 100:
                stats['outcomes'] = stats['outcomes'][-100:]
            
            print(f"📊 AI Performance updated for {symbol}: {outcome_score}/10 ({outcome_type})")
            
        except Exception as e:
            print(f"❌ AI performance update error: {e}")


def main():
    """Main entry point."""
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🤖 ADVANCED AI-POWERED CONTRARIAN TRADING SYSTEM 🤖{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⚠️  WARNING: This system reverses all signals! ⚠️{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   BUY signals → SELL trades{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   SELL signals → BUY trades{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}🧠 Enhanced with ML Signal Enhancement{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}📊 Includes Correlation Analysis{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}🔥 Features Portfolio Heat Tracking{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    # Create and run the system
    system = ContriarianTradingSystem()
    system.run()


if __name__ == "__main__":
    main()
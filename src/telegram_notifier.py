#!/usr/bin/env python3
"""
Telegram Notifier for Contrarian Trading System

Sends real-time trading notifications via Telegram.
"""

import os
import requests
from datetime import datetime
from colorama import Fore, Style


class TelegramNotifier:
    """
    Telegram Notification Handler
    
    Sends trading notifications, alerts, and system status updates.
    """
    
    def __init__(self):
        """Initialize Telegram notifier."""
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.chat_ids = self._parse_chat_ids(os.getenv('TELEGRAM_CHAT_ID', ''))
        self.enabled = os.getenv('TELEGRAM_ENABLED', 'False').lower() == 'true'
        
        if self.enabled and self.bot_token and self.chat_ids:
            print(f"📱 Telegram configured for {len(self.chat_ids)} recipient(s)")
        elif self.enabled:
            print("⚠️ Telegram enabled but missing token or chat ID")
        
    def _parse_chat_ids(self, chat_id_string):
        """Parse chat IDs from environment variable."""
        if not chat_id_string:
            return []
        
        # Handle single ID or comma-separated IDs
        chat_ids = [id.strip() for id in chat_id_string.split(',') if id.strip()]
        return chat_ids
    
    def send_message(self, message, parse_mode='HTML'):
        """Send message to all configured chat IDs."""
        if not self.enabled or not self.bot_token or not self.chat_ids:
            return False
        
        success_count = 0
        
        for chat_id in self.chat_ids:
            try:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                
                payload = {
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': parse_mode,
                    'disable_web_page_preview': True
                }
                
                response = requests.post(url, json=payload, timeout=10)
                
                if response.status_code == 200:
                    success_count += 1
                else:
                    print(f"❌ Telegram send failed for chat {chat_id}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Telegram error for chat {chat_id}: {str(e)}")
        
        if success_count > 0:
            print(f"📱 Telegram message sent to {success_count}/{len(self.chat_ids)} recipients")
            return True
        else:
            print("❌ Failed to send Telegram message to any recipients")
            return False
    
    def send_trade_alert(self, symbol, action, entry_price, sl_price, tp_price, lot_size, reversed=False):
        """Send trade execution alert."""
        if not self.enabled:
            return False
        
        reversal_emoji = "🔄" if reversed else "➡️"
        reversal_text = " (CONTRARIAN)" if reversed else ""
        
        message = f"""🎯 <b>TRADE EXECUTED{reversal_text}</b>

📊 <b>Pair:</b> {symbol}
{reversal_emoji} <b>Action:</b> {action}
💰 <b>Entry:</b> {entry_price:.5f}
🛑 <b>Stop Loss:</b> {sl_price:.5f}
🎯 <b>Take Profit:</b> {tp_price:.5f}
📦 <b>Lot Size:</b> {lot_size}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC"""

        return self.send_message(message)
    
    def send_system_status(self, status, details=""):
        """Send system status update."""
        if not self.enabled:
            return False
        
        status_emoji = "🚀" if "start" in status.lower() else "🛑" if "stop" in status.lower() else "ℹ️"
        
        message = f"""{status_emoji} <b>SYSTEM STATUS</b>

<b>Status:</b> {status}
<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC

{details}"""

        return self.send_message(message)
    
    def send_signal_alert(self, symbol, signal_type, strength, confluences):
        """Send signal generation alert."""
        if not self.enabled:
            return False
        
        strength_emoji = "🔥" if strength >= 8.0 else "⭐"
        
        message = f"""📡 <b>SIGNAL GENERATED</b>

📊 <b>Pair:</b> {symbol}
🔥 <b>Action:</b> {signal_type}
{strength_emoji} <b>Strength:</b> {strength}/10
🎯 <b>Confluences:</b> {len(confluences)}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC"""

        return self.send_message(message)
    
    def test_connection(self):
        """Test Telegram connection."""
        if not self.enabled or not self.bot_token or not self.chat_ids:
            print("❌ Telegram not properly configured")
            return False
        
        test_message = f"""🔧 <b>TELEGRAM TEST</b>

✅ Connection test successful!
📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC

Contrarian Trading System is ready to send notifications."""

        return self.send_message(test_message)
    
    def send_tp_hit_notification(self, symbol, action, entry_price, exit_price, profit_pips, reversed=False):
        """Send take profit hit notification."""
        if not self.enabled:
            return False
        
        reversal_emoji = "🔄" if reversed else "➡️"
        reversal_text = " (CONTRARIAN)" if reversed else ""
        
        message = f"""🎯 <b>TAKE PROFIT HIT{reversal_text}</b>

📊 <b>Pair:</b> {symbol}
{reversal_emoji} <b>Action:</b> {action}
💰 <b>Entry:</b> {entry_price:.5f}
🎯 <b>Exit:</b> {exit_price:.5f}
💵 <b>Profit:</b> +{profit_pips:.1f} pips

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
🎊 <b>Status:</b> TARGET ACHIEVED! 🎊"""

        return self.send_message(message)
    
    def send_sl_hit_notification(self, symbol, action, entry_price, exit_price, loss_pips, reversed=False):
        """Send stop loss hit notification."""
        if not self.enabled:
            return False
        
        reversal_emoji = "🔄" if reversed else "➡️"
        reversal_text = " (CONTRARIAN)" if reversed else ""
        
        message = f"""🛑 <b>STOP LOSS HIT{reversal_text}</b>

📊 <b>Pair:</b> {symbol}
{reversal_emoji} <b>Action:</b> {action}
💰 <b>Entry:</b> {entry_price:.5f}
🛑 <b>Exit:</b> {exit_price:.5f}
📉 <b>Loss:</b> -{loss_pips:.1f} pips

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
🔐 <b>Status:</b> RISK MANAGED"""

        return self.send_message(message)

    def send_priority_trade_notification(self, symbol, signal_type, signal_strength, message):
        """Send priority trade notification."""
        priority_message = f"""
🚨 PRIORITY TRADE EXECUTED 🚨

💎 Symbol: {symbol}
📈 Signal: {signal_type}
⭐ Strength: {signal_strength:.1f}/10
🔥 Status: {message}

⚡ This was the STRONGEST signal available!
💰 Risk: $5 fixed per trade
📊 Max 2 concurrent trades allowed
🛡️ Professional risk management active
        """
        
        return self.send_message(message)
        
    def send_reversal_close_notification(self, symbol, action, entry_price, exit_price, pips):
        """Send reversal close notification."""
        if not self.enabled:
            return False
        
        message = f"""🚨 <b>TRADE CLOSED ON REVERSAL</b>

📊 <b>Pair:</b> {symbol}
🔄 <b>Action:</b> {action}
💰 <b>Entry:</b> {entry_price:.5f}
🚪 <b>Exit:</b> {exit_price:.5f}
📊 <b>Result:</b> {pips:+.1f} pips

🔄 <b>Reason:</b> Major reversal signal detected
⚡ <b>Action:</b> Position closed for risk management

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC"""

        return self.send_message(message)
        
    def send_enhanced_trade_alert(self, symbol, action, entry_price, levels, lot_size, signal_strength, reversed=False):
        """Send enhanced trade entry notification with multiple TP levels."""
        if not self.enabled:
            return False
            
        reversal_emoji = "🔄" if reversed else "➡️"
        reversal_text = " (CONTRARIAN)" if reversed else ""
        
        message = f"""🎯 <b>ENHANCED TRADE EXECUTED{reversal_text}</b>

📊 <b>Pair:</b> {symbol}
{reversal_emoji} <b>Action:</b> {action}
💰 <b>Entry:</b> {entry_price:.5f}
📦 <b>Lot Size:</b> {lot_size}
⭐ <b>Signal Strength:</b> {signal_strength:.1f}/10

📈 <b>ENHANCED TP/SL LEVELS:</b>
🛑 <b>Stop Loss:</b> {levels['sl_price']:.5f}
🎯 <b>TP1:</b> {levels['tp1_price']:.5f} (50%)
🎯 <b>TP2:</b> {levels['tp2_price']:.5f} (30%)  
🎯 <b>TP3:</b> {levels['tp3_price']:.5f} (20%)

⚡ <b>Session Multiplier:</b> {levels['session_multiplier']:.2f}
💪 <b>Strength Multiplier:</b> {levels['strength_multiplier']:.2f}
🎯 <b>Final Multiplier:</b> {levels['final_multiplier']:.2f}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC"""
        
        return self.send_message(message)
        
    def send_enhanced_tp_hit_notification(self, symbol, action, entry_price, exit_price, profit_pips, tp_level, close_percent, contrarian=False):
        """Send enhanced TP hit notification."""
        if not self.enabled:
            return False
            
        contrarian_text = " (CONTRARIAN)" if contrarian else ""
        
        message = f"""🎯 <b>{tp_level} HIT!{contrarian_text}</b>

📊 <b>Pair:</b> {symbol}
🎯 <b>Action:</b> {action}
💰 <b>Entry:</b> {entry_price:.5f}
💰 <b>Exit:</b> {exit_price:.5f}
💵 <b>Profit:</b> +{profit_pips:.1f} pips
📊 <b>Position Closed:</b> {close_percent}%

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
🎯 <b>Status:</b> PARTIAL PROFIT TAKEN"""

        return self.send_message(message)
    
    def send_volume_trade_notification(self, symbol, action, entry_price, levels, signal_strength, volume_score, confluences):
        """Send volume-based trade notification."""
        if not self.enabled:
            return False
        
        confluences_text = "\n".join([f"• {conf}" for conf in confluences[:8]])  # Show top 8
        
        message = f"""🚀 <b>HIGH VOLUME TRADE EXECUTED</b>

📊 <b>Pair:</b> {symbol}
🎯 <b>Action:</b> {action}
💰 <b>Entry:</b> {entry_price:.5f}
📈 <b>Volume Score:</b> {volume_score:.1f}/10 (HIGH)
⭐ <b>Signal Strength:</b> {signal_strength:.1f}/10

🛑 <b>Stop Loss:</b> {levels['sl']:.5f}
🎯 <b>TP1:</b> {levels['tp1']:.5f}
🎯 <b>TP2:</b> {levels['tp2']:.5f}
🎯 <b>TP3:</b> {levels['tp3']:.5f}

📊 <b>Volume Multiplier:</b> {levels['volume_multiplier']:.2f}x

🔗 <b>Confluences:</b>
{confluences_text}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
💡 <b>Strategy:</b> Volume-Based Direct Execution"""

        return self.send_message(message)


def main():
    """Test the Telegram notifier."""
    notifier = TelegramNotifier()
    print("📱 Testing Telegram Notifier...")
    
    if notifier.enabled:
        print("Testing connection...")
        notifier.test_connection()
    else:
        print("Telegram notifications disabled or not configured")


if __name__ == "__main__":
    main()

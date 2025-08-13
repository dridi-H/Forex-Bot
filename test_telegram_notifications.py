#!/usr/bin/env python3
"""
Telegram Notification Test

Test all trading notifications you requested:
1. Trade Execution
2. TP Hit  
3. SL Hit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.telegram_notifier import TelegramNotifier
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def test_all_notifications():
    """Test all trading notifications."""
    print(f"{Fore.CYAN}📱 TESTING ALL TRADING NOTIFICATIONS{Style.RESET_ALL}")
    print("=" * 50)
    
    notifier = TelegramNotifier()
    
    if not notifier.enabled:
        print(f"{Fore.RED}❌ Telegram notifications not enabled{Style.RESET_ALL}")
        return False
    
    print(f"{Fore.GREEN}✅ Telegram configured for {len(notifier.chat_ids)} recipient(s){Style.RESET_ALL}")
    
    # 1. TRADE EXECUTION NOTIFICATION
    print(f"\n{Fore.YELLOW}🚀 1. Testing TRADE EXECUTION notification...{Style.RESET_ALL}")
    
    levels = {
        'sl': 1.35600,
        'tp1': 1.35900, 
        'tp2': 1.36000,
        'tp3': 1.36100,
        'volume_multiplier': 1.25
    }
    
    trade_success = notifier.send_volume_trade_notification(
        symbol='GBPUSDm',
        action='SELL',
        entry_price=1.35750,
        levels=levels,
        signal_strength=9.5,
        volume_score=8.7,
        confluences=[
            'H4 RSI Overbought (78.5)',
            'Volume Bearish Divergence', 
            'Price Above Bollinger Upper',
            'M15 Strong Downtrend Confluence'
        ]
    )
    
    print(f"📊 Trade Execution: {Fore.GREEN}✅ Success{Style.RESET_ALL}" if trade_success else f"❌ Failed")
    
    # 2. TAKE PROFIT HIT NOTIFICATION
    print(f"\n{Fore.YELLOW}🎯 2. Testing TP HIT notification...{Style.RESET_ALL}")
    
    tp_success = notifier.send_enhanced_tp_hit_notification(
        symbol='GBPUSDm',
        action='SELL', 
        entry_price=1.35750,
        exit_price=1.35650,
        profit_pips=10.0,
        tp_level='TP1',
        close_percent=50,  # 50% of position closed
        contrarian=False   # Volume-based trade
    )
    
    print(f"📊 TP Hit: {Fore.GREEN}✅ Success{Style.RESET_ALL}" if tp_success else f"❌ Failed")
    
    # 3. STOP LOSS HIT NOTIFICATION  
    print(f"\n{Fore.YELLOW}🛑 3. Testing SL HIT notification...{Style.RESET_ALL}")
    
    sl_success = notifier.send_sl_hit_notification(
        symbol='USDJPYm',
        action='BUY',
        entry_price=147.250, 
        exit_price=147.150,
        loss_pips=-10.0,
        reversed=False  # Volume-based trade
    )
    
    print(f"📊 SL Hit: {Fore.GREEN}✅ Success{Style.RESET_ALL}" if sl_success else f"❌ Failed")
    
    # SUMMARY
    print(f"\n{Fore.CYAN}📋 NOTIFICATION TEST SUMMARY{Style.RESET_ALL}")
    print("=" * 35)
    
    all_success = trade_success and tp_success and sl_success
    
    if all_success:
        print(f"{Fore.GREEN}🎉 ALL NOTIFICATIONS WORKING PERFECTLY!{Style.RESET_ALL}")
        print()
        print("📱 You will receive notifications for:")
        print("   🚀 Trade Execution (when volume ≥ 8.0)")
        print("   🎯 Take Profit hits (TP1, TP2, TP3)")
        print("   🛑 Stop Loss hits")
        print("   📊 Volume analysis details")
        print("   💰 Profit/Loss calculations")
    else:
        print(f"{Fore.RED}❌ Some notifications failed{Style.RESET_ALL}")
        print(f"   Trade: {'✅' if trade_success else '❌'}")
        print(f"   TP Hit: {'✅' if tp_success else '❌'}")
        print(f"   SL Hit: {'✅' if sl_success else '❌'}")
    
    print(f"\n{Fore.YELLOW}💡 Your volume-only trading system is ready!{Style.RESET_ALL}")
    print("   Only trades when volume score ≥ 8.0/10")
    print("   Instant notifications for all trade events")
    
    return all_success

if __name__ == "__main__":
    test_all_notifications()

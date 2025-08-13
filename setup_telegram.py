#!/usr/bin/env python3
"""
Telegram Setup Helper

This script helps you set up Telegram notifications for the trading system.
"""

import os
from colorama import Fore, Style, init

init(autoreset=True)

def setup_telegram():
    """Guide user through Telegram setup."""
    print(f"{Fore.CYAN}📱 TELEGRAM NOTIFICATIONS SETUP{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}\n")
    
    print("To enable Telegram notifications, you need:")
    print("1. 🤖 A Telegram Bot Token")
    print("2. 💬 Your Chat ID")
    print("3. 🔧 Environment variables set\n")
    
    print(f"{Fore.YELLOW}📋 Steps to get your Bot Token:{Style.RESET_ALL}")
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot command")
    print("3. Choose a name and username for your bot")
    print("4. Copy the bot token (looks like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)")
    
    print(f"\n{Fore.YELLOW}📋 Steps to get your Chat ID:{Style.RESET_ALL}")
    print("1. Start a chat with your new bot")
    print("2. Send any message to the bot")
    print("3. Go to: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
    print("4. Look for 'chat':{'id': YOUR_CHAT_ID}")
    
    print(f"\n{Fore.GREEN}🔧 Setting up Environment Variables:{Style.RESET_ALL}")
    
    # Get user input
    bot_token = input("Enter your Bot Token: ").strip()
    chat_id = input("Enter your Chat ID: ").strip()
    
    if bot_token and chat_id:
        # Create .env file
        env_content = f"""# Telegram Configuration
TELEGRAM_BOT_TOKEN={bot_token}
TELEGRAM_CHAT_ID={chat_id}
TELEGRAM_ENABLED=true

# Trading Configuration
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server

# Risk Management
LOT_SIZE=0.01
MAX_TRADES_PER_DAY=7
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
            
        print(f"\n{Fore.GREEN}✅ .env file created successfully!{Style.RESET_ALL}")
        
        # Test the connection
        print(f"\n{Fore.CYAN}🧪 Testing Telegram connection...{Style.RESET_ALL}")
        
        # Set environment variables for this session
        os.environ['TELEGRAM_BOT_TOKEN'] = bot_token
        os.environ['TELEGRAM_CHAT_ID'] = chat_id
        os.environ['TELEGRAM_ENABLED'] = 'true'
        
        # Test notification
        try:
            import sys
            sys.path.append('src')
            from telegram_notifier import TelegramNotifier
            
            notifier = TelegramNotifier()
            success = notifier.test_connection()
            
            if success:
                print(f"{Fore.GREEN}✅ Telegram notifications are working!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}🔄 Restart your trading system to enable notifications{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Telegram test failed. Check your bot token and chat ID.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error testing Telegram: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Bot token and Chat ID are required{Style.RESET_ALL}")

def show_current_status():
    """Show current Telegram configuration status."""
    print(f"{Fore.CYAN}📱 CURRENT TELEGRAM STATUS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*30}{Style.RESET_ALL}\n")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print(f"{Fore.GREEN}✅ .env file found{Style.RESET_ALL}")
        
        # Load and display settings
        with open('.env', 'r') as f:
            content = f.read()
            if 'TELEGRAM_BOT_TOKEN' in content:
                print(f"{Fore.GREEN}✅ Bot token configured{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Bot token missing{Style.RESET_ALL}")
                
            if 'TELEGRAM_CHAT_ID' in content:
                print(f"{Fore.GREEN}✅ Chat ID configured{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Chat ID missing{Style.RESET_ALL}")
                
            if 'TELEGRAM_ENABLED=true' in content:
                print(f"{Fore.GREEN}✅ Telegram enabled{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️ Telegram disabled{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ .env file not found{Style.RESET_ALL}")
        
    print(f"\n{Fore.CYAN}📋 Notification Types:{Style.RESET_ALL}")
    print("• 🎯 Trade Entry Alerts")
    print("• 💰 Take Profit Hit Notifications")
    print("• 🛑 Stop Loss Hit Notifications")
    print("• 📊 Signal Generation Alerts")
    print("• 🔧 System Status Updates")

if __name__ == "__main__":
    print(f"{Fore.CYAN}🚀 CONTRARIAN TRADING SYSTEM - TELEGRAM SETUP{Style.RESET_ALL}\n")
    
    while True:
        print("\nChoose an option:")
        print("1. 📱 Setup Telegram Notifications")
        print("2. 📊 Show Current Status")
        print("3. 🧪 Test Telegram Connection")
        print("4. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            setup_telegram()
        elif choice == '2':
            show_current_status()
        elif choice == '3':
            try:
                import sys
                sys.path.append('src')
                from telegram_notifier import TelegramNotifier
                notifier = TelegramNotifier()
                notifier.test_connection()
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        elif choice == '4':
            print(f"{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice{Style.RESET_ALL}")

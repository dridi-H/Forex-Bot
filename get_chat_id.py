#!/usr/bin/env python3
"""
Quick Telegram Setup Helper

Get your Chat ID easily for the Dridix Bot
"""

import requests
import json

def get_chat_id():
    """Get your chat ID from Telegram."""
    bot_token = "8282830182:AAGyUw0BUEGdws6jz8Ma9PS5BBGoI8ssg4o"
    
    print("🤖 Dridix Bot - Chat ID Setup")
    print("=" * 35)
    print()
    print("📱 STEP 1: Open Telegram and find your bot:")
    print("   Bot Link: https://t.me/Dridix_bot")
    print("   Bot Username: @Dridix_bot")
    print()
    print("💬 STEP 2: Start a conversation with your bot:")
    print("   - Click 'START' or send any message")
    print("   - Send a simple message like 'hello'")
    print()
    print("🔍 STEP 3: Press Enter after sending the message to get your Chat ID")
    
    input("Press Enter after you've sent a message to your bot...")
    
    # Get updates from Telegram
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok') and data.get('result'):
            updates = data['result']
            if updates:
                # Get the most recent chat
                latest_update = updates[-1]
                chat = latest_update.get('message', {}).get('chat', {})
                chat_id = chat.get('id')
                first_name = chat.get('first_name', 'Unknown')
                
                if chat_id:
                    print(f"\n✅ SUCCESS! Your Chat ID is: {chat_id}")
                    print(f"👤 Name: {first_name}")
                    print(f"\n📋 Add this to your .env file:")
                    print(f"TELEGRAM_CHAT_ID={chat_id}")
                    
                    # Update .env file automatically
                    try:
                        with open('.env', 'r') as f:
                            content = f.read()
                        
                        # Replace the placeholder
                        updated_content = content.replace(
                            'TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE',
                            f'TELEGRAM_CHAT_ID={chat_id}'
                        )
                        
                        with open('.env', 'w') as f:
                            f.write(updated_content)
                        
                        print(f"✅ .env file updated automatically!")
                        
                        # Test the notification
                        print(f"\n🧪 Testing notification...")
                        test_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                        test_data = {
                            'chat_id': chat_id,
                            'text': '🚀 Dridix Bot Connected Successfully!\n\n✅ Your volume-only trading system is ready!\n💡 The bot will notify you when volume ≥ 8.0/10',
                            'parse_mode': 'HTML'
                        }
                        
                        test_response = requests.post(test_url, json=test_data, timeout=10)
                        if test_response.json().get('ok'):
                            print(f"✅ Test notification sent successfully!")
                            print(f"📱 Check your Telegram for the test message")
                        else:
                            print(f"❌ Test notification failed")
                            
                    except Exception as e:
                        print(f"⚠️ Manual setup needed: {e}")
                        
                else:
                    print(f"❌ Could not find chat ID in the response")
            else:
                print(f"❌ No messages found. Make sure you sent a message to the bot first.")
        else:
            print(f"❌ Error getting updates: {data}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    get_chat_id()

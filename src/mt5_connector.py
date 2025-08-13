#!/usr/bin/env python3
"""
MetaTrader 5 Connector

Simple, reliable MT5 connection handler for the contrarian trading system.
"""

import MetaTrader5 as mt5
from colorama import Fore, Style


class MT5Connector:
    """
    MetaTrader 5 Connection Handler
    
    Provides a simple interface for MT5 operations.
    """
    
    def __init__(self):
        """Initialize MT5 connector."""
        self.connected = False
        
    def connect(self, login=None, password=None, server=None):
        """Connect to MT5."""
        try:
            if not mt5.initialize():
                print(f"❌ MT5 initialization failed: {mt5.last_error()}")
                return False
            
            if login and password and server:
                if not mt5.login(login, password, server):
                    print(f"❌ MT5 login failed: {mt5.last_error()}")
                    return False
            
            self.connected = True
            print(f"{Fore.GREEN}✅ MT5 connected successfully{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"❌ MT5 connection error: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from MT5."""
        try:
            mt5.shutdown()
            self.connected = False
            print(f"{Fore.YELLOW}🔌 MT5 disconnected{Style.RESET_ALL}")
        except Exception as e:
            print(f"❌ MT5 disconnect error: {str(e)}")
    
    def get_symbol_info(self, symbol):
        """Get symbol information."""
        try:
            return mt5.symbol_info(symbol)
        except Exception as e:
            print(f"❌ Error getting symbol info for {symbol}: {str(e)}")
            return None
    
    def get_tick(self, symbol):
        """Get current tick for symbol."""
        try:
            return mt5.symbol_info_tick(symbol)
        except Exception as e:
            print(f"❌ Error getting tick for {symbol}: {str(e)}")
            return None
    
    def get_rates(self, symbol, timeframe, count):
        """Get historical rates."""
        try:
            # Convert string timeframe to MT5 constant
            timeframe_map = {
                'M1': mt5.TIMEFRAME_M1,
                'M5': mt5.TIMEFRAME_M5,
                'M15': mt5.TIMEFRAME_M15,
                'M30': mt5.TIMEFRAME_M30,
                'H1': mt5.TIMEFRAME_H1,
                'H4': mt5.TIMEFRAME_H4,
                'D1': mt5.TIMEFRAME_D1,
                'W1': mt5.TIMEFRAME_W1,
                'MN1': mt5.TIMEFRAME_MN1
            }
            
            if isinstance(timeframe, str):
                tf = timeframe_map.get(timeframe, mt5.TIMEFRAME_H1)
            else:
                tf = timeframe
                
            return mt5.copy_rates_from_pos(symbol, tf, 0, count)
        except Exception as e:
            print(f"❌ Error getting rates for {symbol}: {str(e)}")
            return None
    
    def is_connected(self):
        """Check if connected to MT5."""
        return self.connected and mt5.terminal_info() is not None


def main():
    """Test the MT5 connector."""
    connector = MT5Connector()
    print("🔌 Testing MT5 Connector...")
    
    if connector.connect():
        print("MT5 connector test successful!")
        connector.disconnect()
    else:
        print("MT5 connector test failed!")


if __name__ == "__main__":
    main()

from fetch_kline import fetch_kline

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    
    if lowered == 'bot commands' or lowered == '1':
        return 'Additional Bot commands:\n1. Bot commands\n2. Show current RSI\n3. About project creation'
    
    if lowered == 'show current rsi' or lowered == '2':
        return fetch_kline()
    
    if lowered == 'about project creation' or lowered == '3':
        return 'The project was to create the Bot that sends RSI each hour. It was the real fun to develope it, because I have never created a Bot for Discord and used ByBit API.\nP.S. That was a bit confusing at first, but I managed. Difficulties tried to smash me, but failed :)'
    

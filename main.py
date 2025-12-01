import asyncio
import threading
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def run_backend():
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=False, log_level="info")

def run_telegram_bot():
    from telegram_bot import main as bot_main
    bot_main()

if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    asyncio.get_event_loop().run_until_complete(asyncio.sleep(2))
    
    run_telegram_bot()

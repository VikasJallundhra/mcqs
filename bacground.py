import requests
import threading
import time

def keep_awake():
    while True:
        try:
            requests.get("https://mcqs.onrender.com/generate-mcqs")
            print("Server Pinged ✅")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(10)  # Ping every 10 minutes

# Start the self-pinging thread
threading.Thread(target=keep_awake, daemon=True).start()

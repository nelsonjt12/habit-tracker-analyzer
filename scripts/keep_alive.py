import requests
import time
import os
from datetime import datetime

# URL of your Render deployment
URL = "https://habit-tracker-analyzer.onrender.com"

def ping_application():
    try:
        start_time = time.time()
        response = requests.get(URL)
        elapsed = time.time() - start_time
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = response.status_code
        
        print(f"[{timestamp}] Status: {status}, Response time: {elapsed:.2f}s")
        
        # Log to file
        with open("keep_alive_log.txt", "a") as f:
            f.write(f"[{timestamp}] Status: {status}, Response time: {elapsed:.2f}s\n")
            
        return True
    except Exception as e:
        print(f"Error pinging {URL}: {str(e)}")
        return False

def main():
    print(f"Starting keep-alive service for {URL}")
    print("Press Ctrl+C to stop")
    
    # Ping every 10 minutes (600 seconds)
    # This is frequent enough to prevent most free tier services from spinning down
    interval = 600
    
    try:
        while True:
            ping_application()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nKeep-alive service stopped.")

if __name__ == "__main__":
    main()

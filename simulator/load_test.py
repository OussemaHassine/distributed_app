# simulator/load_test.py

import asyncio
import websockets
import random

URI = "ws://localhost:8080"
NUM_CLIENTS = 100

async def simulate_client(user_id: int):
    username = f"User_{user_id:03}"

    # Random startup delay to desync client startup
    await asyncio.sleep(random.uniform(0.1, 2.0))

    while True:
        try:
            async with websockets.connect(URI, ping_interval=3, ping_timeout=2) as ws:
                print(f"✅ {username} connected")
                while True:
                    msg = f"[{username}] Hello from client {user_id}"
                    await ws.send(msg)
                    print(f"📤 Sent: {msg}")
                    await asyncio.sleep(random.uniform(1.5, 4.0))  # randomized message interval
        except Exception as e:
            print(f"🔌 {username} disconnected: {e}. Reconnecting in a few seconds...")
            await asyncio.sleep(random.uniform(2, 5))  # jittered reconnect delay

async def main():
    tasks = [simulate_client(i) for i in range(1, NUM_CLIENTS + 1)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

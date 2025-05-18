# server/chat_server.py

import asyncio
import websockets
import redis.asyncio as redis
from shared.config import REDIS_HOST, REDIS_PORT, CHANNEL_NAME

connected_clients = set()

async def handle_client(websocket):
    connected_clients.add(websocket)
    print("🟢 Client connected")
    try:
        async for message in websocket:
            print(f"📨 Received: {message}")
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
            await r.publish(CHANNEL_NAME, message)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        connected_clients.remove(websocket)
        print("🔴 Client disconnected")

async def start_server(port):
    async with websockets.serve(
        handle_client,
        "localhost",
        port,
        ping_interval=None,
        ping_timeout=None
    ):
        print(f"🚀 Chat server running on ws://localhost:{port}")
        await asyncio.Future()

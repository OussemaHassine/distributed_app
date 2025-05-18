# server/redis_subscriber.py

import asyncio
import redis.asyncio as redis
from shared.config import REDIS_HOST, REDIS_PORT, CHANNEL_NAME

async def listen_to_redis(connected_clients):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    pubsub = r.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)
    print(f"📡 Subscribed to Redis channel: {CHANNEL_NAME}")

    async for message in pubsub.listen():
        if message['type'] == 'message':
            text = message['data'].decode()
            print(f"🔁 Broadcasting: {text}")
            print(f"👀 Connected clients at this moment: {len(connected_clients)}")
            
            dead_clients = []
            for client in connected_clients.copy():
                try:
                    await client.send(text)
                except Exception as e:
                    print(f"❌ Error sending to client: {e}")
                    dead_clients.append(client)
            for client in dead_clients:
                connected_clients.remove(client)

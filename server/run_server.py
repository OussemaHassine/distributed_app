# server/run_server.py

import asyncio
import sys
from server.chat_server import start_server, connected_clients
from server.redis_subscriber import listen_to_redis

async def main(port):
    await asyncio.gather(
        start_server(port),
        listen_to_redis(connected_clients)
    )

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 6789
    asyncio.run(main(port))

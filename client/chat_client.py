# client/chat_client.py

import asyncio
import websockets

async def chat():
    uri = "ws://localhost:8080"

    async def connect():
        while True:
            try:
                ws = await websockets.connect(uri, ping_interval=3, ping_timeout=2)
                return ws
            except Exception as e:
                print(f"🔄 Connection failed: {e}. Retrying in 3s...")
                await asyncio.sleep(3)

    async def send(ws):
        print("✅ Connected to ws://localhost:8080")
        while True:
            try:
                msg = await asyncio.to_thread(lambda: input("> You: "))

                await ws.send(msg)
            except Exception as e:
                break

        

    async def receive(ws):
        try:
            async for message in ws:
                print(f"🔁 {message}\n> ", end="")
        except Exception:
            pass

    async def run():
        while True:
            ws = await connect()
            sender = asyncio.create_task(send(ws))
            receiver = asyncio.create_task(receive(ws))

            done, pending = await asyncio.wait(
                [sender, receiver],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            print("\n🔌 Connection lost. Attempting to reconnect...")

    await run()

if __name__ == "__main__":
    asyncio.run(chat())

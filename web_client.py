import websockets
import asyncio
import logging

logging.basicConfig(level=logging.INFO)


async def consumer_handler(websocket: websockets.WebSocketClientProtocol) -> None:
    async for message in websocket:
        log_message(message)
    
async def consume(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}/broker"
    async with websockets.connect(websocket_resource_url) as websocket:
        await consumer_handler(websocket)

def log_message(message: str) -> None:
    logging.info(f"Message: {message}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(hostname="195.134.67.142", port=6001))
    loop.run_until_complete(consume(hostname="195.134.67.142", port=6002))
    loop.run_until_complete(consume(hostname="195.134.67.142", port=6003))
    loop.run_until_complete(consume(hostname="195.134.67.142", port=6004))
    loop.run_forever()

import asyncio
import websockets
import json

async def produce_one(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()

async def produce_two(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()


#message='WebSocket message! for the port 6000.'
message = {
    "message_type":"Alert",
    "speed": "15",
    "distance": "3"
}
message = json.dumps(message)
#asyncio.get_event_loop().run_until_complete(produce(message='hi', host='localhost', port=4000))
#asyncio.get_event_loop().run_forever()
#asyncio.run(produce_one(message, host='195.134.67.142', port=7000))
asyncio.run(produce_two(message, host='195.134.67.142', port=6001))
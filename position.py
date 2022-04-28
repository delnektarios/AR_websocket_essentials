import asyncio
import json
import websockets

async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()


message = {
    "message_type":"position_data",
    "latitude":"48.1706",
    "longitude":"11.2479", 
    "item":"ambulance", 
    "speed":"16km/h", 
    "distance":"5m"
}
message = json.dumps(message)
asyncio.run(produce(message, host='195.134.67.142', port=7000))
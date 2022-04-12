import asyncio
import json
import websockets

async def produce_one(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()

async def produce_two(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()



message = {
    "message_type":"Mission_Init",
    "mission_id":"20000",
    "timestamp":"1614182460315",
    "mission_title":"Risk Alert",
    "mission_description":"Unidentified vehicle is approaching restricted area",
    "mission_status":"ACTIVE"
}
message = json.dumps(message)
asyncio.run(produce_two(message, host='195.134.67.142', port=6005))
import asyncio
import websockets

async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()



message='This is the p again.'
#asyncio.get_event_loop().run_until_complete(produce(message='hi', host='localhost', port=4000))
#asyncio.get_event_loop().run_forever()
asyncio.run(produce(message, host='127.0.0.1', port=13000))
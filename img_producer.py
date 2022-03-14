import asyncio
import websockets
import base64

async def produce_one(image_path: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        with open(image_path, "rb") as image_file: 
            encoded_string = base64.b64encode(image_file.read())
        # printing the size of the encoded image which is sent
        print("Encoded size of the sent image: {0} bytes".format(len(encoded_string)))

        await ws.send(encoded_string)
        await ws.recv()

asyncio.run(produce_one("./image.jpg", host='195.134.67.142', port=6000))
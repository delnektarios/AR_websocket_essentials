import asyncio
import websockets
import base64
import json

async def produce_one(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()

with open("./image.jpg", "rb") as image_file: 
    encoded_string = base64.b64encode(image_file.read())
    # printing the size of the encoded image which is sent
    print("Encoded size of the sent image: {0} bytes".format(len(encoded_string)))

#video source https://dl.dropboxusercontent.com/s/d4f4v2df1lhtz5q/DEMO%201%2027-36%281%29%281%29.mp4
# video stream source = (the beach) http://212.170.100.189/mjpg/video.mjpg
message = {
    "message_type":"Multimedia",
    "media_id":"000",
    "timestamp":"1614182460315",
    "media_type":"videostream",
    "media_title":"Baby Image",
    "media_text":"This is a baby!",
    "datastream":"",
    "media_source":"http://212.170.100.189/mjpg/video.mjpg",
    "media_status":"ALERT_ACTIVE",
}
message = json.dumps(message)
asyncio.run(produce_one(message, host='195.134.67.142', port=6004))
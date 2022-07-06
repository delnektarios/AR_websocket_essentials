from asyncio.events import get_event_loop
from asyncio.streams import start_server
import websockets
import asyncio
import logging
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)

class Server:
    
    clients = set()

    async def register(self, ws:WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects. ")

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects. ")
    
    async def send_to_clients(self, message: str) -> None:
        if self.clients:
        #we dont want that now
        #if False:
            await asyncio.wait([client.send(message) for client in self.clients])
    
    async def ws_handler(self, ws: WebSocketServerProtocol, url: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        except:
            logging.exception("Something is not valid to happen")
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(message)

server = Server()
alert_socket = websockets.serve(server.ws_handler, '195.134.67.142', 6001)
sthad_initializer = websockets.serve(server.ws_handler, '195.134.67.142', 6007)
#message_socket = websockets.serve(server.ws_handler, '195.134.67.142', 6002)
#tweet_socket = websockets.serve(server.ws_handler, '195.134.67.142', 6003)
#multimedia_socket = websockets.serve(server.ws_handler, '195.134.67.142', 6004)
#mission_socket = websockets.serve(server.ws_handler, '195.134.67.142', 6005)
#position_socket = websockets.serve(server.ws_handler, '195.134.67.142', 7000)
loop = get_event_loop()
loop.run_until_complete(alert_socket)
loop.run_until_complete(sthad_initializer)
#loop.run_until_complete(message_socket)
#loop.run_until_complete(tweet_socket)
#loop.run_until_complete(multimedia_socket)
#loop.run_until_complete(mission_socket)
#loop.run_until_complete(position_socket)
loop.run_forever()

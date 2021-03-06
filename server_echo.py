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
start_server = websockets.serve(server.ws_handler, '195.134.67.142', 6000)
loop = get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()



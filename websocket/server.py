import asyncio
import websockets
from utils import json_error, get_status
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import defaultdict

# TODO set FILE/IP/PORT for the websocket
FILE = "/data/status_kfet.json"
IP = "0.0.0.0"
PORT = 80

class UpdateHandler(FileSystemEventHandler):

    def __init__(self, f):
        super().__init__()
        self.connected = []

    async def send(self, msg):
        for i, ws in enumerate(self.connected):
            try : 
                await ws.send(msg)
            except websockets.ConnectionClosed:
                self.connected[i] = False
        
        # remove all disconnected webscockets 
        self.connected = list(filter((lambda connected: connected), self.connected))

    def on_modified(self, event):
        status = get_status(FILE)
 
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send(status))

event_handler = UpdateHandler(FILE)

async def update(websocket, path):
    event_handler.connected.append(websocket)

    # init connection by sending the current
    # status
    await websocket.send(get_status(FILE))

    while True:
        await asyncio.sleep(1) 

if __name__=="__main__":

    websocket = websockets.serve(update, IP, PORT)
    loop = asyncio.get_event_loop()
    observer = Observer()
    observer.schedule(event_handler, "/data")
    observer.start()
    
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket)
    loop.run_forever()

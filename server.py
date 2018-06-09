import asyncio
import websockets
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import defaultdict

FILE = "status_kfet.json"

def json_error():
    print("JSON error : attribute not found")
    return

# load kfet status from json file f
def get_status(f):
    with open(f) as fd:
        kfet = defaultdict(json_error, json.load(fd))
    return kfet["status"]

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
        self.connected = list(filter((lambda connected: not connected), self.connected))

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

websocket = websockets.serve(update, 'localhost', 7800)
loop = asyncio.get_event_loop()
observer = Observer()
observer.schedule(event_handler, "./")
observer.start()

asyncio.set_event_loop(loop)
loop.run_until_complete(websocket)
loop.run_forever()

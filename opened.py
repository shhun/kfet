import asyncio
import websockets
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FILE = "status_kfet.json"

class UpdateHandler(FileSystemEventHandler):

    def __init__(self, f, ws):
        super().__init__()
        self.f = f
        self.ws = ws

    async def send(self, msg):
        await (self.ws).send(msg)

    def on_modified(self, event):
        fd = open(self.f, 'r')
        kfet = json.loads("".join(fd.readlines()))
        content = kfet["status"]
        
        asyncio.get_event_loop().run_until_complete(self.send(content))

async def update(websocket, path):
    while True:
        await asyncio.sleep(0.5) 

websocket = websockets.serve(update, 'localhost', 7800)
loop = asyncio.get_event_loop()
event_handler = UpdateHandler(FILE, websocket)
observer = Observer()
observer.schedule(event_handler, "./")
observer.start()


loop.run_until_complete(websocket)
loop.run_forever()
    
 

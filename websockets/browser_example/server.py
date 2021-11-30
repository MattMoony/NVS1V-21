#!/usr/bin/env python3

import asyncio
import datetime
import random
import websockets

async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)

async def main():
    async with websockets.serve(time, 'localhost', 5678):
        await asyncio.Future()

asyncio.run(main())
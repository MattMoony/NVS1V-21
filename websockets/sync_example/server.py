#!/usr/bin/env python3

import asyncio
import json
import logging
import websockets

logging.basicConfig()

STATE = {'value': 0}
USERS = set()

def state_event():
    return json.dumps({'type': 'state', **STATE})

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def counter(websocket, path):
    try:
        USERS.add(websocket)
        websockets.broadcast(USERS, users_event())
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data['action'] == 'minus':
                STATE['value'] -= 1
                websockets.broadcast(USERS, state_event())
            elif data['action'] == 'plus':
                STATE['value'] += 1
                websockets.broadcast(USERS, state_event())
            else:
                logging.error('unsupported event: %s', data)
    finally:
        USERS.remove(websocket)
        websockets.broadcast(USERS, users_event())

async def __main():
    async with websockets.serve(counter, 'localhost', 6789):
        await asyncio.Future()

def main():
    asyncio.run(__main())

if __name__ == '__main__':
    main()
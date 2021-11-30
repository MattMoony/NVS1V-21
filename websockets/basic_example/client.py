#!/usr/bin/env python3

import asyncio
import websockets as ws

async def hello():
    uri = 'ws://localhost:8765'
    async with ws.connect(uri) as sock:
        name = input('Name: ')
        await sock.send(name)
        print(f'[>] "{name}"')
        res = await sock.recv()
        print(f'[<] "{res}"')

def main():
    asyncio.run(hello())

if __name__ == '__main__':
    main()
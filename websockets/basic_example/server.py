#!/usr/bin/env python3

import asyncio
import websockets as ws

async def hello(sock, path):
    name = await sock.recv()
    print(f'[<] "{name}"')
    await sock.send(f'Hello {name}!')
    print(f'[>] "Hello {name}!"')

async def __main():
    async with ws.serve(hello, 'localhost', 8765):
        await asyncio.Future()

def main():
    asyncio.run(__main())

if __name__ == '__main__':
    main()
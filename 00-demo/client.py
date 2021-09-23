#!/usr/bin/env python3

import sys
import socket
import select
from typing import *
import colorama as cr
from queue import Queue, Empty
from argparse import ArgumentParser

cr.init()

"""The maximum number of characters that can be read from stdin at once"""
MAX_IN: int     = 0x1ff
"""The default buffer size"""
BUF_SZ: int     = 0x400

def main():
    parser = ArgumentParser()
    parser.add_argument('host', type=str, help='Specify the server\'s hostname ... ')
    parser.add_argument('port', type=int, help='Specify the server\'s port ... ')
    args = parser.parse_args()

    client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setblocking(1)
    client.connect((args.host, args.port))
    client.setblocking(0)

    inputs: List[socket.socket] = [ sys.stdin.fileno(), client.fileno(), ]
    outputs: List[socket.socket] = [ client.fileno(), ]
    queue: Queue = Queue()

    try:
        while True:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s == sys.stdin.fileno():
                    msg: str = sys.stdin.readline()[:MAX_IN].strip()
                    print(f'{cr.Fore.LIGHTBLUE_EX}{":".join(str(x) for x in client.getsockname())}> {msg}{cr.Fore.RESET}')
                    queue.put(msg.encode())
                else:
                    buf: bytes = client.recv(BUF_SZ)
                    if buf:
                        print(f'\r{buf.decode().strip()}')
                    else:
                        client.close()
                        print('[*] Server closed connection - shutting down ... ')
                        break
            if writable:
                try:
                    msg = queue.get_nowait()
                    client.send(msg)
                except (Empty, KeyError):
                    pass
            if exceptional:
                client.close()
                print('[*] Server closed connection - shutting down ... ')
                break
    except KeyboardInterrupt:
        print('[*] Shutting down gracefully ... ')
        client.close()

if __name__ == '__main__':
    main()
#!/usr/bin/env python3

import os
import socket
import select
import sqlite3
from typing import *
from queue import Queue, Empty
from argparse import ArgumentParser

"""The absolute path to the directory this script is in"""
BPATH: str      = os.path.abspath(os.path.dirname(__file__))
"""The maximum number of connection requests to queue until refusing new ones"""
MAX_REQ: int    = 5
"""The name of the default room"""
DEF_ROOM: str   = 'global'
"""The default buffer size"""
BUF_SZ: int     = 0x400

# def init_db(db_path: str, sql_path: str = os.path.join(BPATH, 'setup.sql')) -> None:
#     """Initializes the SQLite3 database"""
#     con: sqlite3.Connection = sqlite3.connect(db_path)
#     cur: sqlite3.Cursor = con.cursor()
#     with open(sql_path, 'r') as f:
#         cur.executescript(f.read())
#     con.close()

def main():
    parser = ArgumentParser()
    parser.add_argument('host', type=str, help='Specify the server\'s hostname ... ')
    parser.add_argument('port', type=int, help='Specify the server\'s port ... ')
    # parser.add_argument('--db', type=str, help='Path to SQLite3 db (default = in memory) ... ', default=':memory:')
    args = parser.parse_args()

    # if args.db == ':memory:' or not os.path.isfile(args.db):
    #     init_db(args.db)

    print('[*] Starting up ... ')
    server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind((args.host, args.port))
    server.listen(MAX_REQ)
    print(f'[*] Now listening on {args.host}:{args.port} ... ')

    inputs: List[socket.socket] = [ server, ]
    outputs: List[socket.socket] = [ ]
    rooms: Dict[socket.socket, str] = dict()
    addrs: Dict[socket.socket, Tuple[str, int]] = dict()
    queues: Dict[str, Dict[socket.socket, Queue]] = { DEF_ROOM: dict(), }

    try:
        while True:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s is server:
                    conn, addr = s.accept()
                    conn.setblocking(0)
                    inputs.append(conn)
                    outputs.append(conn)
                    queues[DEF_ROOM][conn] = Queue()
                    addrs[conn] = addr
                    rooms[conn] = DEF_ROOM
                    print(f'[*] Opened connection to {":".join(str(x) for x in addr)} ... ')
                else:
                    buf: bytes = s.recv(BUF_SZ)
                    if buf:
                        for _, q in filter(lambda q: q[0] != s, queues[rooms[s]].items()):
                            q.put((addrs[s], buf))
                    else:
                        outputs.remove(s)
                        inputs.remove(s)
                        del queues[rooms[s]][s]
                        del rooms[s]
                        del addrs[s]
                        s.close()
                        print(f'[*] Closed connection to {":".join(str(x) for x in addr)} ... ')
            for s in writable:
                try:
                    saddr, msg = queues[rooms[s]][s].get_nowait()
                    s.send(b':'.join(str(x).encode() for x in saddr) + b'> ' + msg)
                except (Empty, KeyError):
                    pass
            for s in exceptional:
                outputs.remove(s)
                inputs.remove(s)
                del queues[rooms[s]][s]
                del rooms[s]
                del addrs[s]
                s.close()
                print(f'[*] Closed errorneous connection to {":".join(str(x) for x in addr)} ... ')
    except KeyboardInterrupt:
        print('[*] Exiting gracefully ... ')

if __name__ == '__main__':
    main()
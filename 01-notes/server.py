#!/usr/bin/env python3

import json
import asyncio
import datetime
import websockets as ws
import websockets.server
from typing import *

from lib import db
from lib.events import Events
from lib.models.note import Note

mutex: asyncio.Lock = asyncio.Lock()
users: Set[websockets.server.WebSocketServerProtocol] = set()
notes: List[Note] = []

async def get_id(sock: websockets.server.WebSocketServerProtocol, data: Dict[str, Any]) -> None:
    """Generates a new ID for a new note"""
    async with mutex:
        await sock.send(Events.new_id(int(datetime.datetime.now().timestamp() * 1_000)))
        await asyncio.sleep(.001)

async def save_note(sock: websockets.server.WebSocketServerProtocol, data: Dict[str, Any]) -> None:
    """Saves a newly created / edited note"""
    if any(x not in data.keys() for x in ('id', 'title', 'body',)):
        return
    try:
        note = next(filter(lambda n: n.id == data['id'], notes))
        note.title = data['title']
        note.body = data['body']
    except:
        notes.append(Note(data['id'], data['title'], data['body']))
    db.write(notes)
    ws.broadcast(users, Events.notes(notes))

async def delete_note(sock: websockets.server.WebSocketServerProtocol, data: Dict[str, Any]) -> None:
    """Deletes the given note"""
    if 'id' not in data.keys():
        return
    try:
        del notes[notes.index(next(filter(lambda n: n.id == data['id'], notes)))]
        db.write(notes)
        ws.broadcast(users, Events.notes(notes))
    except Exception as e:
        print(e)
        pass

hndlr: Dict[str, Callable[[websockets.server.WebSocketServerProtocol, Dict[str, Any]], None]] = {
    'get_id': get_id,
    'save': save_note,
    'delete': delete_note,
}

async def loop(sock: websockets.server.WebSocketServerProtocol, path: str):
    try:
        print(f'[*]: New connection from {sock.remote_address} ... ')
        users.add(sock)
        ws.broadcast(users, Events.users(users))
        await sock.send(Events.notes(notes))
        async for msg in sock:
            data: Dict[str, Any] = json.loads(msg)
            await hndlr[data['action']](sock, data)
            
    finally:
        print(f'[*]: Closed connection to {sock.remote_address} ... ')
        users.remove(sock)
        ws.broadcast(users, Events.users(users))

async def main():
    print(f'[*]: websockets version = {ws.version.version} ... ')
    async with ws.serve(loop, 'localhost', 6789):
        await asyncio.Future()

if __name__ == '__main__':
    notes = db.init()
    asyncio.run(main())

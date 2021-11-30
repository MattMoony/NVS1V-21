import json
import websockets as ws
from typing import *

from lib.models.note import Note

class Events(object):
    
    @classmethod
    def users(cls, users: Set) -> str:
        return json.dumps({ 'type': 'users', 'count': len(users), })

    @classmethod
    def notes(cls, notes: List[Note]) -> str:
        return json.dumps({ 'type': 'notes', 'notes': [ n.dumps() for n in notes ] })

    @classmethod
    def new_id(cls, _id: int) -> str:
        return json.dumps({ 'type': 'id', 'id': _id, })

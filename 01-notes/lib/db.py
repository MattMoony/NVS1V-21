import os
import json
from typing import *

from lib.models.note import Note

BPATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NPATH: str = os.path.join(BPATH, 'notes.json')

def init() -> List[Note]:
    if not os.path.isfile(NPATH):
        write([])
        return []
    else:
        return read()

def write(notes: List[Note]) -> None:
    with open(NPATH, 'w') as f:
        json.dump([ n.dumps() for n in notes ], f)

def read() -> List[Note]:
    with open(NPATH, 'r') as f:
        notes = json.load(f)
    return [ Note.loads(n) for n in notes ]

from typing import *

class Note(object):
    def __init__(self, id: int, title: str = '', body: str = ''):
        self.id: int = id
        self.title: str = title
        self.body: str = body

    def dumps(self) -> Dict[str, Any]:
        return dict(id=self.id, title=self.title, body=self.body)

    @classmethod
    def loads(cls, json: Dict[str, Any]) -> "Note":
        if any(x not in json.keys() for x in ('id', 'title', 'body',)):
            return None
        return Note(json['id'], json['title'], json['body'])
import os, json
from typing import *

from demo.models.user import User
from demo.models.datastore import DataStore

class JsonStore(DataStore):
    """Stores the user data in a JSON file"""

    def __init__(self, fname: str):
        """
        Creates a new JSON store.
        :param fname: The filename of the JSON file
        """
        self.fname: str = fname
        self.users: Set[User] = set()

        if not os.path.isdir(os.path.dirname(fname)):
            os.makedirs(os.path.dirname(fname))
        if not os.path.isfile(fname):
            with open(fname, 'w') as f:
                json.dump(list(self.users), f)
        else:
            self.load()

    def load(self) -> None:
        """
        Load all users from the store again.
        """
        with open(self.fname, 'r') as f:
            self.users = set([User.load(o) for o in json.load(f)])
    
    def store(self, user: User) -> None:
        """
        Stores a user in the JSON file.
        :param user: The user to-be-stored
        """
        self.users.add(user)
        with open(self.fname, 'w') as f:
            json.dump([u.dump() for u in self.users], f)
    
    def get(self, name: str) -> Optional[User]:
        """
        Gets a user by their username.
        :param name: The username
        """
        fil: List[User] = list(filter(lambda u: u.name == name, self.users))
        return fil[0] if fil else None

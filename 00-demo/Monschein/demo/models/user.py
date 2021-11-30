from typing import *
from hashlib import sha512

class User(object):
    """Represents a user of the application"""

    def __init__(self, name: str, passw: Optional[str] = None, 
                 hashed: Optional[bytes] = None):
        """
        Creates a new User object.
        :param name: The username
        :param passw: The password
        :param hashed: The hashed password
        """
        self.name: str = name
        self.hashed: bytes = hashed if hashed else sha512(passw.encode()).digest()

    @classmethod
    def load(cls, obj: Dict[str, Any]) -> None:
        """Convert JSON dictionary to object"""
        return User(obj['username'], hashed=bytes.fromhex(obj['password']))

    def dump(self) -> Dict[str, Any]:
        """Convert object to JSON dictionary"""
        return dict(username=self.name, password=self.hashed.hex())

    def check(self, pw: str) -> bool:
        """Checks whether the given password is correct"""
        return sha512(pw.encode()).digest() == self.hashed

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        return self.name == other.__name__

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f'User("{self.name}")'

from typing import *

class User(object):
    """Represents a user of the application"""

    def __init__(self, name: str, passw: str):
        """
        Creates a new User object.
        :param name: The username
        :param passw: The password
        """
        self.name: str = name
        self.passw: str = passw

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        return self.name == other.__name__

    def __str__(self) -> str:
        return f'User("{self.name}")'

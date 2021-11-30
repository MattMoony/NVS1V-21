#!/usr/bin/env python3

from typing import *
import colorama as cr
from demo.models.user import User
from demo.models.datastore import DataStore

class Console(object):
    """Represents the console for interaction with the user"""
    
    def __init__(self, cmds: Dict[str, Callable[..., None]], store: DataStore, prompt: str = '> '):
        """
        Create a new `Console` object.
        :param cmds: A dictionary with all cmds and their handlers
        :param prompt: The prompt to display in front of user input
        """
        self.cmds: Dict[str, Callable[..., None]] = cmds
        self.store: DataStore = store
        self.prompt: str = prompt
        self.user: Optional[User] = None
    
    def run(self) -> None:
        """
        Loop forever, handling user input.
        """
        try:
            while True:
                cmd: str = input(f'{cr.Fore.LIGHTBLUE_EX}{self.user.name if self.user else ""}{self.prompt}{cr.Fore.RESET}')
                args: List[str] = cmd.split()
                tmp: Union[Callable[..., None], Dict[str, Callable[..., None]]] = self.cmds
                i: int = 0
                try:
                    while type(tmp) == dict:
                        tmp = tmp[args[i]]
                        i += 1
                    tmp(self, *args[i:])
                except KeyError:
                    print(f'[-] Unknown command "{cmd}" ... ')
        except KeyboardInterrupt:
            pass

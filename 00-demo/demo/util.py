from typing import *
import colorama as cr

def __p(c: str, t: str, s: str) -> None:
    """
    Print a message in a colour
    :param c: The colour
    :param t: The symbol in brackets
    :param s: The message
    """
    print(f'{c}[{t}] {s}{cr.Fore.RESET}')

def perror(s: str) -> None:
    """Print an error message"""
    __p(cr.Fore.LIGHTRED_EX, '-', s)

def pwarning(s: str) -> None:
    """Print a warning message"""
    __p(cr.Fore.LIGHTYELLOW_EX, '!', s)

def psuccess(s: str) -> None:
    """Print a success message"""
    __p(cr.Fore.LIGHTGREEN_EX, '+', s)

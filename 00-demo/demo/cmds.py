import os, sys
from typing import *
import colorama as cr
from getpass import getpass

from demo.util import *
from demo.models.user import User
from demo.models.console import Console

def __rec_gen_help(cmds: Dict[str, Any], ind: int = 0) -> str:
    """Helper function to recursively generate the help"""
    return f'\n'.join((f'{" "*ind}{c}: {f.__doc__}' if type(f) != dict else f'{" "*ind}{c}:\n'+__rec_gen_help(f, ind+2)) for c, f in cmds.items())

def __gen_help() -> str:
    """Helper function to generate the help menu"""
    lines: List[str] = __rec_gen_help(CMDS).split('\n')
    return f'demo - help\n{"="*max(map(lambda l: len(l), lines))}\n' +\
            '\n'.join(lines)

def show_help(ctx: Console) -> None:
    """Show this help"""
    print(__gen_help())

def show_users(ctx: Console) -> None:
    """List all users"""
    print('\n'.join(f'- {u}' for u in ctx.store.users))

def do_register(ctx: Console) -> None:
    """Register a new user"""
    username: str = input('Username: ')
    if ctx.store.get(username):
        perror('Username is already taken!')
        return
    while True:
        passw: str = getpass('New Password: ')
        _passw: str = getpass('Confirm new password: ')
        if passw == _passw:
            break
        perror('Passwords don\'t match!')
    ctx.user = User(username, passw)
    ctx.store.store(ctx.user)
    psuccess('New user has been created!')

def do_login(ctx: Console) -> None:
    """Log into a user account"""
    username: str = input('Username: ')
    user: User = ctx.store.get(username)
    if not user:
        perror(f'No user with the name of "{username}" was found!')
        return
    for i in range(3):
        if user.check(getpass('Password: ')):
            break
        perror(f'Wrong password! {3-i-1}/3 tries remaining ...')
    else:
        perror('Too many wrong tries!')
        return
    psuccess(f'Welcome back "{user.name}"!')
    ctx.user = user

def do_logout(ctx: Console) -> None:
    """Log out of the currently used account"""
    ctx.user = None

def do_exit(ctx: Console) -> None:
    """Exit this program"""
    sys.exit(0)

def do_clear(ctx: Console) -> None:
    """Clear the console"""
    os.system('clear' if sys.platform != 'win32' else 'cls')

CMDS: Dict[str, Any] = {
    'help': show_help,
    'show': {
        'users': show_users,
    },
    'register': do_register,
    'login': do_login,
    'logout': do_logout,
    'exit': do_exit,
    'clear': do_clear,
}

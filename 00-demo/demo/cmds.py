from typing import *
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
    pass

def do_login(ctx: Console) -> None:
    """Log into a user account"""
    pass

CMDS: Dict[str, Any] = {
    'help': show_help,
    'show': {
        'users': show_users,
    },
    'register': do_register,
    'login': do_login,
}

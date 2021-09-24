#!/usr/bin/env python3

import os
import colorama as cr
cr.init()
from typing import *
from argparse import ArgumentParser

from demo import cmds
from demo.models.console import Console
from demo.models.jsonstore import JsonStore

"""The absolute path to the directory this file is in"""
BPATH: str = os.path.abspath(os.path.dirname(__file__))

def main():
    parser = ArgumentParser()
    parser.add_argument('--store-name', type=str, help='Path to the store file ... ', 
                        default=os.path.join(BPATH, 'store.json'))
    args = parser.parse_args()

    print("""Welcome to my ... 

██████╗ ███████╗███╗   ███╗ ██████╗ 
██╔══██╗██╔════╝████╗ ████║██╔═══██╗
██║  ██║█████╗  ██╔████╔██║██║   ██║
██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║
██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝
╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ 
    
... hope you enjoy your stay!
""")

    con: Console = Console(cmds.CMDS, JsonStore(args.store_name))
    con.run()

if __name__ == '__main__':
    main()
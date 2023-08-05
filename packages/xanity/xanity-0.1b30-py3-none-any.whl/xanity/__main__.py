#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from .constants import COMMANDS

parser = argparse.ArgumentParser(description='Manage scientific experiments, parameters, and analyses')
parser.add_argument('action', type=str, nargs=1, help='action for xanity to do. ( {} )'.format(COMMANDS.INIT+COMMANDS.SETUP+COMMANDS.RUN+COMMANDS.ANAL))
args, remaining_args = parser.parse_known_args()

# print('args: {}   rem_args:{}'.format(args,remaining_args))
# print('args.action: {}'.format(args.action))

if args.action[0] in COMMANDS.INIT:
    from . import initialize
    initialize.main(remaining_args)
  
elif args.action[0] in COMMANDS.SETUP:
    from . import setup
    setup.main(remaining_args)

elif args.action[0] in COMMANDS.RUN+COMMANDS.ANAL:
    from . import xanity
    xanity.run_hook()
    
elif args.action[0] in COMMANDS.STATUS:
    from . import xanity
    xanity.report_status()

else:
    raise NotImplementedError('xanity did not understand that action')

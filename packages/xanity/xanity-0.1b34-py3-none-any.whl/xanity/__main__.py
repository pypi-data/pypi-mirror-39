#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess

from xanity.setup_env import main as setup
from xanity.initialize import main as initialize
from xanity import xanity
from xanity.constants import COMMANDS, ENV_COMMANDS

if xanity.action == COMMANDS.INIT:
    initialize()

elif xanity.action == COMMANDS.SETUP:
    setup()

elif xanity.action in COMMANDS.RUN + COMMANDS.ANAL:
    xanity.run_hook()

elif xanity.action in COMMANDS.STATUS:
    xanity.report_status()

elif xanity.action in COMMANDS.ID:
    print(xanity.uuid)

elif xanity.action in COMMANDS.ENV:
    if xanity.args.env_action in ENV_COMMANDS.REMOVE:
        print('removing conda env: {}...'.format(xanity.uuid))
        subprocess.check_call(['bash', '-lc', 'conda env remove -n {}'.format(xanity.uuid)])
        print('removed.')

elif callable(getattr(xanity, xanity.action)):
        print(repr(getattr(xanity, xanity.action)()))

sys.exit(0)



# import argparse
# from .constants import COMMANDS
# parser = argparse.ArgumentParser(description='Manage scientific experiments, parameters, and analyses')
# parser.add_argument('action', type=str, nargs=1, help='action for xanity to do. ( {} )'.format(COMMANDS.INIT+COMMANDS.SETUP+COMMANDS.RUN+COMMANDS.ANAL))
# args, remaining_args = parser.parse_known_args()
#
# print('args: {}   rem_args:{}'.format(args,remaining_args))
# print('args.action: {}'.format(args.action))
#
# if args.action[0] in COMMANDS.INIT:
#     from . import initialize
#     initialize.main(remaining_args)
#
# elif args.action[0] in COMMANDS.SETUP:
#     from . import setup
#     setup.main(remaining_args)
#
# elif args.action[0] in COMMANDS.RUN+COMMANDS.ANAL:
#     from . import xanity
#     xanity.run_hook()
#
# elif args.action[0] in COMMANDS.STATUS:
#     from . import xanity
#     xanity.report_status()
#
# else:
#     raise NotImplementedError('xanity did not understand that action')

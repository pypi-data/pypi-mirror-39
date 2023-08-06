#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Barry Muldrey
#
# This file is part of xanity.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import sys
import subprocess

from xanity import xanity
from xanity.setup_env import main as setup
from xanity.initialize import main as initialize
from xanity.constants import COMMANDS, ENV_COMMANDS


xanity._parse_args()

if xanity.action == COMMANDS.INIT:
    initialize()

elif xanity.action == COMMANDS.SETUP:
    setup()

elif xanity.action in COMMANDS.RUN + COMMANDS.ANAL:
    xanity._absolute_trigger()

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

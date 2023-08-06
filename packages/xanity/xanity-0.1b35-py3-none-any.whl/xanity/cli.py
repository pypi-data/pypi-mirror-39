import argparse
import sys
import re
import os

from .constants import COMMANDS, INVOCATION


def parser(xanity, clargs=None):

    xanity.command = ' '.join(sys.argv)

    if clargs:
        list_to_parse = clargs.split(' ') if isinstance(clargs, str) else list(clargs)
    elif xanity.invocation == INVOCATION.IMPORT:
        return None
    else:
        list_to_parse = None


    parser = argparse.ArgumentParser(prog='xanity')
    parser.add_argument('action', nargs='?', help='available actions include: {}'.format(COMMANDS))
    action_arg, remaining_args = parser.parse_known_args(list_to_parse) if list_to_parse else parser.parse_known_args()

    if not action_arg.action in COMMANDS and xanity.invocation == INVOCATION.HOOK:
        hook_action = xanity.resolve_hook_action()
        action_arg.action = hook_action
    else:
        hook_action = False

    if action_arg.action in COMMANDS.RUN:
        # 'run' command parser
        parser.add_argument('experiments', nargs='*',
                            help='specify the experiments to run')
        parser.add_argument('-a', '--and-analyze', nargs='*',
                            help="request that data be analyzed upon completion of experiment")
        parser.add_argument('--debug', action='store_true',
                            help='run experiment in debugging mode; experiment code may print additional output'
                                 ' or behave differently')
        parser.add_argument('--logging', action='store_true',
                            help='request experiment perform additional logging')
        parser.add_argument('--loadcp', action='store_true',
                            help='request experiment look for and load stored checkpoints from src/include/persistent'
                                 ' rather than start from scratch')
        parser.add_argument('--savecp', action='store_true',
                            help='request experiment try to save checkpoints to src/include/persistent'
                                 ' (will NOT overwrite)')
        parser.add_argument('--profile', action='store_true',
                            help='run cProfile attatched to your experiment')

    elif action_arg.action in COMMANDS.ANAL:
        # 'analyze' command parser
        parser.add_argument('runid', nargs='*',
                            help='specify the data-path to analyze')
        parser.add_argument('-a', '--analyses', nargs='*',
                            help="""list of explicit analyses to run""")
        parser.add_argument('--debug', action='store_true',
                            help='run experiment in debugging mode; experiment code may print additional output'
                                 ' or behave differently')
        parser.add_argument('--logging', action='store_true',
                            help='request experiment perform additional logging')
        parser.add_argument('--profile', action='store_true',
                            help='run cProfile attatched to your experiment')

    elif action_arg.action in COMMANDS.INIT:
        # 'initialize' command parser
        parser.add_argument('directory', nargs='?', help='path to location of new or existing xanity project')
        parser.add_argument('--examples', '--with-examples', action='store_true',
                            help='include example experiments and analyses')

    elif action_arg.action in COMMANDS.SETUP:
        parser.add_argument('directory', nargs='?', help='path to location of an existing xanity project')

    elif action_arg.action in COMMANDS.ID:
        parser.add_argument('help', nargs='?', help='print xanity id -- help')

    elif action_arg.action in COMMANDS.ENV:
        parser.add_argument('env_action', help='manipulate the internal conda env')

    xanity.args, xanity.unknownargs = parser.parse_known_args(list_to_parse) if list_to_parse else parser.parse_known_args()
    xanity.args.action = action_arg.action if not hook_action else hook_action



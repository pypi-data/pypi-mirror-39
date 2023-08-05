# -*- coding: utf-8 -*-
from .common import Constants, Alias

RELATIVE_PATHS = Constants({
    'src': 'src/',
    'include': 'include/',
    'experiments': 'experiments/',
    'analyses': 'analyses/',
    'run_data': 'data/runs/',
    'persistent_data': 'data/persistent/',
    'saved_data': 'data/saved/',
    'project_root': '/',
    'xanity_data': '.xanity/',
})

XANITY_FILES = Constants({
    'conda_env': 'conda_environment.yaml',
    'conda_hash': '.xanity/conda.md5',
    'env_hash': '.xanity/env_state.md5',
    'uuid': '.xanity/UUID',
})

COMMANDS = Constants({
    'RUN':    Alias('RUN',    ['RUN', 'run']),
    'ANAL':   Alias('ANAL',   ['ANAL', 'anal', 'analyze', 'analyse', 'analysis', 'analyses']),
    'SETUP':  Alias('SETUP',  ['SETUP', 'setup']),
    'STATUS': Alias('STATUS', ['STATUS', 'status']),
    'INIT':   Alias('INIT',   ['INIT', 'init', 'initialize', 'initialise']),
    'ID':     Alias('ID',     ['ID', 'id', 'uuid', 'ID', 'UUID']),
    'ENV':    Alias('ENV',    ['ENV', 'env', 'environment', 'ENV', 'ENVIRONMENT']),
})

ENV_COMMANDS = Constants({
    'REMOVE': Alias('REMOVE',    ['REMOVE', 'remove', 'rm', 'RM', 'DELETE', 'delete', 'del', 'DEL']),
})

# ACTIONS = Constants({
#     'RUN': 'run',
#     'ANAL': 'anal',
#     'INIT': 'init',
#     'SETUP': 'setup',
#     'STATUS': 'status',
# })

ACTIVITIES = Constants({
    'CONST': 'constructing_xanity_object',
    'ORIENT': 'orienting',
    'EXP': 'experimenting',
    'ANAL': 'analyzing',
    'WAIT': 'waiting',
    'ABORT': 'aborting',
})

DIRNAMES = Constants({
    'SAVED_VARS': "xanity_variables",
})
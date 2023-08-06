#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
from .Xanity import Xanity
from .constants import ACTIVITIES
from .common import get_external_caller

fns_to_expose = [
        'experiment_parameters',
        'associated_experiments',
        'log',
        'save_variable',
        'load_variable',
        'analyze_this',
        'load_checkpoint',
        'save_checkpoint',
        'persistent',
        'report_status',
        'run',
        'find_recent_data',
]

vars_to_expose = [
        'status',
        'logger',
        'project_root',
        ]

thismodule = sys.modules[__name__]

if 'xanity' not in locals():

    # may have to set placeholders because modules which import
    # xanity might have to be imported during the creation of the Xanity object
    xanity = Xanity()

# check frame, register import, check_invocation
tb = traceback.extract_stack(limit=15)
for frame in tb:
    if 'import xanity' in frame[3]:
        xanity._register_import(frame[0])


def _log_and_get(item_name):
    if not xanity.status.act_tags:
        xanity._register_external_access(get_external_caller())
    return getattr(xanity, item_name)


def _xanity_getter(item_name):
    return lambda *args, **kwargs: _log_and_get(item_name)(*args, **kwargs)


for fn in fns_to_expose:
    setattr(thismodule, fn, _xanity_getter(fn))

for var in vars_to_expose:
    setattr(thismodule, var, property(_xanity_getter(var)))




#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
from .Xanity import Xanity

fns_to_expose = [
        'run_hook',
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
]

vars_to_expose = [
        'status',
        'logger',
        ]


def _proxy_method(name):
    return getattr(xanity, name)


thismodule = sys.modules[__name__]

if 'xanity' not in locals():

    xanity = Xanity()

    for item in fns_to_expose:
        setattr(thismodule, item, _proxy_method(item))

    for item in vars_to_expose:
        setattr(thismodule, item, _proxy_method(item))

tb = traceback.extract_stack(limit=15)

for frame in tb:
    if 'import xanity' in frame.line:
        xanity.register_import(frame.filename)


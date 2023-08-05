#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
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

thismodule = sys.modules[__name__]

if 'xanity' not in locals():

    # define placeholder attrs
    for fn in fns_to_expose:
        setattr(thismodule, fn, lambda: None)
    for var in vars_to_expose:
        setattr(thismodule, var, None)
    
    # create xanity object
    xanity = Xanity()

    if xanity.project_root is not None:
             
        # go through and redefine attrs using the real things
        for fn in fns_to_expose:
            setattr(thismodule, fn, getattr(xanity, fn))
        for var in vars_to_expose:
            setattr(thismodule, var, getattr(xanity, var))

        # do the real initialization
        xanity._orient()

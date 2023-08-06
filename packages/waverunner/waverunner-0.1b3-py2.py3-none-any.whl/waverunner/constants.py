# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from .common import Constants

RELATIVE_PATHS = Constants({
    'src':'src/',
    'include':'include/',
    'experiments':'experiments/',
    'analyses':'analyses/',
    'run_data':'data/runs/',
    'persistent_data':'data/persistent/',
    'saved_data':'data/saved/',
    'project_root': '/',
    'xanity_data':'.xanity/',
})

XANITY_FILES = Constants({
    'conda_env': 'conda_environment.yaml',
    'conda_hash':'.xanity/conda.hash',
})

COMMANDS = Constants({
    'RUN': ['run'],
    'ANAL': ['anal', 'analyze', 'analyse', 'analysis', 'analyses'],
    'SETUP': ['setup'],
    'STATUS': ['status'],
    'INIT': ['init', 'initialize','initialise'],
})

ACTIONS = Constants({
    'RUN': 'run',
    'ANAL': 'anal',
    'INIT': 'init',
    'SETUP': 'setup',
    'STATUS': 'status',
})

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
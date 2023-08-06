#
# Module contain handlers for workers module
#
# Copyright (c) 2018, Gavrilov S
# Licensed MIT License.
#

import sys


def get_queue_manager_instance(current_module):
    """
    find queue manager in manager module
    :param current_module: module manager
    :return: Object of QManager class
    """
    for key, value in current_module.__dict__.items():
        if value.__class__.__name__ == 'QManager':
            return value
    raise AttributeError('Object of Qmanager class has not been determined')


def get_file_manager():
    """
    try to get 'manager.py' file in current work directory
    :return:
    """

    try:
        module = __import__('manager')
    except ModuleNotFoundError as exp:
        print(exp)
        sys.exit(1)
    return module

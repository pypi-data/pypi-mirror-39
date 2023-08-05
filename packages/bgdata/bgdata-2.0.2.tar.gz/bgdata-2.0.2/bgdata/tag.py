"""
Tags are files (referenced by the tag name) that contain the
build id of a package.

This module provides utilities to read and write tag files.

.. important:: Tags must begin with an alpha character

The default tag is MASTER.

"""

import logging
import time


MASTER = 'master'
DEVELOP = 'develop'
BUILD = 'build'
DEFAULT = MASTER


def read_build(file, retry=5):
    """Read the build from a tag file"""
    last_error = None
    for retries in range(retry):
        try:
            with open(file) as fd:
                return fd.readlines()[0].strip()
        except Exception as e:
            last_error = e
            logging.getLogger(__name__).debug('Error reading tag file: %s. Retry: %d' % (e, retries))
            # Wait one second and try again
            time.sleep(1)
    raise last_error


def write_build(file, build):
    """Write the build to a tag file. Path must exists"""
    with open(file, 'w') as fd:
        fd.writelines([build])


def is_valid(value):
    return value[0].isalpha()

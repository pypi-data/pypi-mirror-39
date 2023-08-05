"""
In this module we define the package object (an object that contains the project, dataset and version)
and we include utilities to manage how the user interacts with them
(parsing user input 'project/dataset/version?build' and writing the same format back
to the user).

In addition, this module includes de functions to create a package from a set of files
and to extract a compressed package.
"""

import collections
import datetime
import logging
import os
import tarfile
from os import path

from bgdata.errors import PackageError


DEFAULT_PROJECT = '_'

_Package = collections.namedtuple('Package', ['project', 'dataset', 'version'])


class Package(_Package):
    """Package class with project, dataset and version"""

    def __str__(self):
        return '{}/{}/{}'.format(self.project, self.dataset, self.version)

    @property
    def str(self):
        return self.__str__()


def parse(user_str):
    """Parse the user input [<project>/]dataset/version[?build|tag]
    and extract all the fields."""
    if user_str.count('/') == 1:
        req = user_str.split('?')
        dataset, version = req[0].split('/')
        project = DEFAULT_PROJECT
    elif user_str.count('/') == 2:
        req = user_str.split('?')
        project, dataset, version = req[0].split('/')
    else:
        raise PackageError('Invalid str for package')

    if len(req) == 1:
        return project, dataset, version, None
    else:
        return project, dataset, version, req[1]


def stringify_build(package, build):
    """Write the appropriate string for a build of a package"""
    return '{}-{}'.format(package.str, build)


def stringify_tag(package, tag):
    """Write the appropriate string for a tag of a package"""
    return '{}.{}'.format(package, tag)


def stringify(package, ref=None):
    """Write the appropriate string for a build or tag of a package.
    This function should be used when writing back a package to the user"""
    return '{}'.format(package) if ref is None else '{}?{}'.format(package, ref)


COMPRESSION_FORMATS = [".xz", ".gz", ".bz2", ""]


def extract(file, fmt, dest):
    """Extract a compressed data package"""

    logging.getLogger(__name__).info("Extracting %s" % path.basename(file))
    logging.getLogger(__name__).debug('"%s" (with format "%s") is being extrated in "%s"' % (file, fmt, dest))

    with tarfile.open(file, 'r{}'.format(fmt.replace('.', ':'))) as package:

        # Check if it's a single file
        names = package.getnames()

        if len(names) == 1:
            # Create a file to mark this package as singlefile
            with open(path.join(dest, '.singlefile'), 'w') as fd:
                fd.writelines([names[0]])

        # Extract there
        package.extractall(dest)

        # Mark downloaded
        with open(path.join(dest, '.downloaded'), 'w') as fd:
            fd.writelines([str(datetime.datetime.now())])


def compress(f, fmt, dest, exclude_hidden=False):
    """Create a compressed version of a data package"""
    # TODO add filter to change permissions...

    logging.getLogger(__name__).info("Compressing %s" % path.basename(f))
    logging.getLogger(__name__).debug('"%s" (with format "%s") is being compressed in "%s"' % (f, fmt, dest))

    with tarfile.open(dest, 'w{}'.format(fmt.replace('.', ':'))) as package:

        # Check if it's a single file
        if path.isfile(f):
            package.add(f, arcname=path.basename(f))
        else:  # directory
            for dirpath, dirnames, filenames in os.walk(f):
                for file in filenames:
                    if exclude_hidden and file.startswith('.'):
                        continue
                    else:
                        name = path.join(dirpath, file)
                        package.add(name, arcname=name.replace(f, ''))

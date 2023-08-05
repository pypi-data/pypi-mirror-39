import collections
import hashlib
import logging
import bgconfig
import configobj
import sys

from os import path
from validate import Validator

from bgdata.errors import BGDataError


def exception_formatter(exception_type, exception, traceback, others_hook=sys.excepthook):
    """
    Reduce verbosity of error messages associated with your exceptions

    Args:
        others_hook: hook for exceptions of a different class. Default is the system hook

    """
    if issubclass(exception_type, BGDataError):
        logging.getLogger(__name__).error("%s: %s" % (exception_type.__name__, exception))
    else:
        others_hook(exception_type, exception, traceback)


def md5(fname):
    """Compute md5 checksum of a file"""
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def build_config_file(template_file, output_file, output_folder, name):

    # Search for v1 config file
    v1_file = path.join(output_folder, 'bgdata.conf')
    if path.exists(v1_file):
        v1_confspec = path.join(path.dirname(path.abspath(__file__)), 'bgdata.conf.template.spec')
        old_configuration = configobj.ConfigObj(v1_file, configspec=v1_confspec)
        old_configuration.validate(Validator(), preserve_errors=True)

        for key in old_configuration.keys():
            if key not in ['local_repository', 'remote_repository', 'cache_repositories', 'offline', 'version', 'proxy']:
                raise BGDataError('Configuration file error. BGData does not longer support custom builds for packages. '
                                  'Use a separate file for that.')

        if 'cache_repositories' in old_configuration:
            caches_old = old_configuration['cache_repositories']
            caches_new = collections.OrderedDict()
            fmt = 'cache_{{:0{}d}}'.format(len(str(len(caches_old))))

            for i, cache in enumerate(caches_old):
                caches_new[fmt.format(i)] = cache

            del old_configuration['cache_repositories']
            old_configuration['cache_repositories'] = caches_new

        old_configuration.write(open(output_file, 'wb'))

    else:
        bgconfig.copyfile(template_file, output_file)

import logging
import pprint
import sys
from logging import config as loggingconfig

import click

import bgdata
from bgdata import package
from bgdata import tag as tagmod
from bgdata import utils


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class LogInfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', default=False, is_flag=True, help='Give more information')
@click.option('-q', '--quiet', default=False, is_flag=True, help="Suppress all log messages but the ones on stderr")
@click.version_option()
def cmdline(verbose, quiet):
    """Manage data packages"""

    # Re-configure the logging
    logconf = {'version': 1, 'disable_existing_loggers': False,
               'formatters': {'bgdatafmt': {'format': '%(asctime)s %(name)s %(levelname)s -- %(message)s',
                                            'datefmt': '%Y-%m-%d %H:%M:%S'}
                              },
               'filters': {'info': {'()': bgdata.command.LogInfoFilter}},
               'handlers': {
                   'bgout': {
                       'class': 'logging.StreamHandler',
                       'formatter': 'bgdatafmt',
                       'level': 'DEBUG',
                       'stream': 'ext://sys.stdout',
                       'filters': ['info']
                   },
                   'bgerr': {
                       'class': 'logging.StreamHandler',
                       'formatter': 'bgdatafmt',
                       'level': 'WARNING',
                       'stream': 'ext://sys.stderr',
                   },
               },
               'root': {'level': 'WARNING', 'handlers': ['bgout', 'bgerr']}


    }
    if quiet:
        verbose = False
        logconf['loggers'] = {'bgdata': {'level': logging.WARNING}}
    else:
        logconf['loggers'] = {'bgdata': {'level': logging.DEBUG if verbose else logging.INFO}}

    if not verbose:
        sys.excepthook = utils.exception_formatter

    loggingconfig.dictConfig(logconf)


def validate_package(ctx, param, value):
    try:
        package.parse(value)
    except package.PackageError:
        raise click.BadParameter('Invalid package string. Try PROJECT/DATASET/VERSION?BUILD')
    else:
        return value  # Return the value to ensure that the default identifier is set


def validate_tag(ctx, param, value):
    if tagmod.is_valid(value):
        return value
    else:
        raise click.BadParameter('Invalid tag string. Tags cannot start with a non-digit character')


def validate_build(ctx, param, value):
    if not tagmod.is_valid(value):
        return value
    else:
        raise click.BadParameter('Invalid tag string. Tags cannot start with a non-digit character')


@cmdline.command(short_help='Get a data package')
@click.argument('pkg', metavar='<PACKAGE>', callback=validate_package)
@click.option('-f', '--force', default=False, is_flag=True, help="Force to download the package even in offline mode")
def get(pkg, force):
    """
    <PACKAGE> = [<project>]/<dataset>/<version>[?<tag>|<build>]

    Get the path of a certain <PACKAGE>. If the package is not present,
    it will be downloaded if available.

    \b
    If project is not indicated, the default project is assumed: '_'
    If build or tag are not indicated, default tag is assumed: 'master'
    """

    logging.getLogger('bgdata').debug('Get: Package %s -- Force: %s' % (pkg, force))

    # Create a manager
    downloader = bgdata.Manager(forceonline=force)

    dataset_path = downloader.get(pkg)

    logging.getLogger('bgdata').info("Dataset downloaded")

    print(dataset_path)


@cmdline.command(short_help='Create a data package')
@click.argument('f', metavar='<FILE or DIR>', nargs=1, type=click.Path(exists=True))
@click.argument('pkg', metavar='<PACKAGE>', callback=validate_package)
@click.option('-c', '--compression', type=click.Choice(package.COMPRESSION_FORMATS), default='.xz', help='Compression format')
@click.option('-e', '--exclude-hidden', default=False, is_flag=True, help='Exclude hidden files from the build')
def build(f, pkg, compression, exclude_hidden):
    """
    <PACKAGE> = [<project>/]<dataset>/<version>[?<build>]

    From a file or directory (<FILE or DIR>) create a compressed data package.

    \b
        $ bgdata build myfolder project/dataset/version

    After the build is done, an extracted copy is set in the local repository that can be used
    for testing. The tag "build" can be used to refer to the built package.

    \b
    If project is not indicated in <PACKAGE>, the default project is assumed: '_'
    If build is not indicated in <PACKAGE>, a build with the current date is used
    """

    logging.getLogger('bgdata').debug('Build: Package %s -- Input %s' % (pkg, f))

    # Create a manager
    builder = bgdata.Manager()

    pkg_ = builder.build(pkg, f, fmt=compression, exclude_hidden=exclude_hidden)

    print(pkg_)


@cmdline.command(short_help='Upload a local built package to remote')
@click.argument('pkg', metavar='<PACKAGE>', callback=validate_package)
@click.option('-p', '--project', default=None, help='Override package project in the remote')
@click.option('-d', '--dataset', default=None, help='Override package dataset in the remote')
@click.option('-v', '--version', default=None, help='Override package version in the remote')
@click.option('-b', '--build', default=None, help='Override package build in the remote', callback=validate_build)
@click.option('-t', '--tag', default=None, help='Associate the build with a particular tag in the remote', callback=validate_tag)
@click.option('-m', '--message', 'description', default=None, help='Description for the package')
def upload(pkg, project, dataset, version, build, tag, description):
    """
    <PACKAGE> = [<project>]/<dataset>/<version>[?<build>]

    Upload a built <PACKAGE> to the remote. <PACKAGE> must have been build previously

    \b
    If project is not indicated, the default project is assumed: '_'
    If build or tag are not indicated, default tag is assumed: 'master'"""

    logging.getLogger('bgdata').debug('Upload: Package {}'.format(pkg))

    # Create a manager
    uploader = bgdata.Manager()

    pkg_ = uploader.upload(pkg, project=project, datastet=dataset, version=version, build=build, tag=tag, description=description)

    print(pkg_)


@cmdline.group(short_help='Manage packages in the caches')
def cache():
    """Manage packages in the caches"""
    pass


@cache.command(short_help='Add a package to the caches')
@click.argument('pkg', metavar='<PACKAGE>', callback=validate_package)
@click.option('-c', '--cache', 'caches', default=None, multiple=True, help='Cache name to apply to')
def add(pkg, caches):
    """
    <PACKAGE> = [<project>]/<dataset>/<version>[?<tag>|<build>]

    Add a package to the caches

    \b
        $ bgdata cache add project/dataset/version

    By default, the operation is applied to all caches.
    If you want to apply only to some caches, you can indicate them by name.

    \b
        $ bgdata cache add project/dataset/version -c cache1 -c cache2"""

    logging.getLogger('bgdata').debug('Add to caches: Package %s -- To %s' % (pkg, caches))

    # Create a manager
    cache_manager = bgdata.Manager()

    if len(caches) == 0:
        cache_manager.cache_add(pkg)
    else:
        cache_manager.cache_add(pkg, caches)


@cache.command(short_help='Remove a package from the caches')
@click.argument('pkg', metavar='<PACKAGE>', callback=validate_package)
@click.option('-c', '--cache', 'caches', default=None, multiple=True, help='Cache name to apply to')
def remove(pkg, caches):
    """
    <PACKAGE> = [<project>]/<dataset>/<version>[?<tag>|<build>]

    Remove a package from the caches

    \b
        $ bgdata cache remove project/dataset/version

    By default, the operation is applied to all caches.
    If you want to apply only to some caches, you can indicate them by name.

    \b
        $ bgdata cache remove project/dataset/version -c cache1 -c cache2"""

    logging.getLogger('bgdata').debug('Remove from caches: Package %s -- To %s' % (pkg, caches))

    # Create a manager
    cache_manager = bgdata.Manager()

    if len(caches) == 0:
        cache_manager.cache_remove(pkg)
    else:
        cache_manager.cache_remove(pkg, caches)


@cache.command(short_help='Clean everything in the cache')
@click.option('-c', '--cache', 'caches', default=None, multiple=True, help='Name of the caches')
def clean(caches):
    """Clean all the files and directories in the cache directory

    Warning! Everything will be removed, even if it does not belong
    to a data package, so use with care

    By default, the operation is applied to all caches.
    If you want to apply only to some caches, you can indicate them by name.

    \b
        $ bgdata cache clean -c cache1 -c cache2"""

    logging.getLogger('bgdata').debug('Clean caches: %s' % (caches, ))

    # Create a manager
    cache_manager = bgdata.Manager()

    if len(caches) == 0:
        cache_manager.cache_clean()
    else:
        cache_manager.cache_clean(caches)


@cache.command(short_help='Update packages in the cache')
@click.option('-t', '--tag', 'tags', default=None, multiple=True, help='Name of the tags')
@click.option('-c', '--cache', 'caches', default=None, multiple=True, help='Name of the caches')
def update(tags, caches):
    """Packages updated according to builds from some tags

    If not tags are provided, the default is the "master" tag.
    You can provide as many tags as you wish:

    \b
        $ bgdata cache update -t master -t develop

    If a cache contains a build of a certain package,
    it will be removed if is not in the tags
    and add the builds from those tags will be added to the cache.

    IMPORTANT:

    \b
    - if the cache lacks a package this command will not add it
    - builds of packages that are not in the tags will be removed

    By default, the operation is applied to all caches.
    If you want to apply only to some caches, you can indicate them by name.

    \b
        $ bgdata cache update -c cache1 -c cache2
    """

    logging.getLogger('bgdata').debug('Update caches: %s using %s' % (caches, tags))

    # Create a manager
    cache_manager = bgdata.Manager()

    kw = {}

    if len(caches) > 0:
        kw['caches'] = caches
    if len(tags) > 0:
        kw['tags'] = tags

    cache_manager.cache_update(**kw)


@cmdline.command(short_help='List local packages')
@click.option('-t', '--no-tags', 'tags', default=False, is_flag=True, help="Do not show tags associated with the package")
@click.option('-c', '--no-cache', 'cache', default=False, is_flag=True, help='Do not list packages in the caches')
def list(tags, cache):
    """List packages in the local repository"""

    logging.getLogger('bgdata').debug('List: -- Tags %s -- Caches %s' % (tags, cache))

    # Create a manager
    lister = bgdata.Manager()

    for query, name, tags in lister.list(exclude_caches=cache, exclude_tags=tags):
        print('{}\t\t{}\t\t{}'.format(query, name, tags))


@cmdline.command(short_help='Search for a package')
@click.argument('query', metavar='<QUERY>', required=False)
@click.option('-l', '--local', default=False, is_flag=True, help='Search in the local repo')
def search(query, local):
    """
    <QUERY> = [<project>[/<dataset>[/<version>[?<build>]]]]

    Search for a package in the remote (or local) repository.
    You can search for projects, datasets, or versions or builds
    """

    logging.getLogger('bgdata').debug('Search: -- Query %s -- Local %s' % (query, local))

    # Create a manager
    searcher = bgdata.Manager()

    for item in searcher.search(query, local=local):
        print(item)


@cmdline.command(short_help='Read metadata of a package (in the remote)')
@click.argument('query', metavar='<QUERY>', required=True)
def info(query):
    """
    <QUERY> = <project>[/<dataset>[/<version>[?<build>]]]

    Read metadata information in the remote.
    This command reads the metadata of a project, dataset, version
    or build of a package.
    """

    logging.getLogger('bgdata').debug('Info: -- Query %s' % query)

    # Create a manager
    informer = bgdata.Manager()

    info_ = informer.info(query)

    if info_ is not None:
        pprint.pprint(info_)


if __name__ == "__main__":
    cmdline()

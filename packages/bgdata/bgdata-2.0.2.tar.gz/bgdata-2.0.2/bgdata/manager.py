"""
The Manager is the high level interface for the user to manage his/her data packages

In this code we make use of the term ref to refer to an string that represents a build or tag
(but we do not know yet what is it).

Some of the methods have a "protected" version that instead of accepting the new
string format (project/dataset/version?ref) use the old format style
(project, dataset, version, ref).
"""

import collections
import datetime
import logging
import os
import configobj

from os import path as mpath
from bgconfig import BGConfig

from bgdata import package as mpackage, utils
from bgdata import repository
from bgdata import tag as mtag
from bgdata.errors import BGDataError, PackageNotFoundError, PackageError, TagNotFound


class Manager:

    def __init__(self, forceonline=False, builds_file=None):

        self.config = BGConfig(mpath.join(mpath.dirname(__file__), "bgdatav2.conf.template"), build_hook=utils.build_config_file)
        if forceonline:
            self.offline = False
        elif 'BGDATA_OFFLINE' in os.environ:
            self.offline = True if os.environ.get('BGDATA_OFFLINE').upper() in ['TRUE', 'YES'] else False
        else:
            self.offline = self.config.get("offline", False)
        self.local = repository.Local(os.environ.get("BGDATA_LOCAL", self.config['local_repository']), self.config['cache_repositories'], offline=self.offline)
        self.remote = repository.Remote(os.environ.get("BGDATA_REMOTE", self.config['remote_repository']), path=self.config.get('remote_repository_upload', None), proxy=self.config.get('proxy', None))
        self.one_time_warnings = collections.defaultdict(set)
        self.default_tag = os.environ.get("BGDATA_TAG", mtag.DEFAULT)
        builds_file = os.environ.get("BGDATA_BUILDS", None) if builds_file is None else builds_file
        self._custom_builds = {} if builds_file is None else \
            configobj.ConfigObj(infile=builds_file, configspec=mpath.join(mpath.dirname(__file__), "builds.conf.template.spec"))

# Downloader

    def _custom_path(self, pkg):
        """Check if package is in a custom folder.
        Return None if no custom folder is present or if the custom folder does not exits"""

        key = pkg.str
        path = self._custom_builds.get('paths', {}).get(key, None)
        if path is not None:  # custom path is always returned

            if key not in self.one_time_warnings['path']:
                if mpath.exists(path):
                    logging.getLogger(__name__).warning("Using a custom path '%s' at %s" % (path, key))
                else:
                    logging.getLogger(__name__).warning("Custom path '%s' for %s not found. Skipped" % (path, key))
                self.one_time_warnings['path'].add(key)

            if mpath.exists(path):
                return path

        return None

    def _custom_tag(self, pkg):
        """Check if there is a custom tag.
        Return None if there is not custom tag"""
        key = pkg.str
        custom_tags = self._custom_builds.get('tags', {})
        if key in custom_tags:
            tag = custom_tags[key]
        elif key.rsplit('/', 1)[0] in custom_tags:
            tag = custom_tags[key.rsplit('/', 1)[0]]
        elif key.split('/', 1)[0] in custom_tags:
            tag = custom_tags[key.split('/', 1)[0]]
        else:
            tag = None
        return tag

    def _custom_build(self, pkg, tag):
        """Check if there is build for a particular tag.
        Return None if no custom build is exits"""

        key = pkg.str
        custom_config = self._custom_builds.get('builds', {}).get(key, {})
        if tag in custom_config:  # custom build overrides default tag (master)
            build = custom_config['{}'.format(tag)]
            if '.'.join([key, tag]) not in self.one_time_warnings['build']:
                logging.getLogger(__name__).warning("Using a custom build '%s' at %s for tag %s" % (build, key, tag))
            self.one_time_warnings['build'].add('.'.join([key, tag]))

            return build

        return None

    def _tag2build(self, pkg, tag):
        """Get the build associated to a tag"""

        logging.getLogger(__name__).debug('Search for tag "%s" of "%s"' % (tag, pkg))

        local_tag_error = None
        remote_tag_error = None

        build = None

        # Look for a local tag
        build_local = None
        try:
            build_local = self.local.read_tag(pkg, tag)
        except Exception as e:
            local_tag_error = e

        # Look for remote tag
        if not self.offline:
            timeout = 20.0 if build_local is None else 1.0
            try:
                build = self.remote.read_tag(pkg, tag, timeout=timeout)
            except Exception as e:
                remote_tag_error = e
            else:
                key = pkg.str
                if build is None and build_local is not None and (key, tag) not in self.one_time_warnings['tag']:  # can be only a local tag
                    logging.getLogger(__name__).warning('Unable to find %s.%s in remote. Using local' % (key, tag))
                    self.one_time_warnings['tag'].add((key, tag))

        if build is not None:  # build found in the remote
            if build != build_local:  # if our local is not up to date (or not present)
                self.local.write_tag(pkg, build=build, tag=tag)
            logging.getLogger(__name__).info('Tag "%s" for "%s" resolved as %s' % (tag, pkg, build))
        elif build_local is not None:  # build only in the local
            # if we cannot get the latest from the remote (may be we are offline) use the local build
            build = build_local
            logging.getLogger(__name__).info('Tag "%s" for "%s" resolved as %s' % (tag, pkg, build))
        else:
            err_msg = 'Tag {} for package {} not found'.format(tag, pkg)
            if remote_tag_error is not None:
                err_msg += " ({})".format(remote_tag_error)
            elif local_tag_error is not None:
                err_msg += " ({})".format(local_tag_error)
            raise TagNotFound(err_msg)

        return build

    def _ref2build(self, pkg, ref):
        """Get the build associated with a ref."""
        build = None
        if ref is None:
            ref = self._custom_tag(pkg)
        ref = ref if ref is not None else self.default_tag
        # Check whether the ref is a tag or a build
        if mtag.is_valid(ref):  # if is a valid tag
            build = self._custom_build(pkg, ref)
            if build is None:
                build = self._tag2build(pkg, ref)
        else:
            build = ref
        return build

    def _get_path(self, pkg, build):
        """Get the data package from a build. If online mode is enabled
        and package is not present it will be downloaded"""

        # Check if it's at local
        local_path = self.local.get(pkg, build)

        if local_path is None:

            if self.offline:  # Build not found
                logging.getLogger(__name__).error('Package "%s-%s" not found locally. Offline mode is set, try forcing the download.' % (pkg, build))
                err_msg = 'Package {}-{} not found'.format(pkg, build)
                raise PackageNotFoundError(err_msg)
            else:
                logging.getLogger(__name__).info('Package "%s-%s" not found in local repo' % (pkg, build))
                # Download it from remote
                local_path = self.local.get_path(pkg, build)
                checksum = self.remote.get_checksum(pkg, build)
                self.remote.download(local_path, pkg, build, checksum=checksum)

        # Check if it's a single file
        if mpath.exists(mpath.join(local_path, '.singlefile')):
            with open(mpath.join(local_path, '.singlefile')) as fd:
                file_name = fd.readlines()[0].strip()
                local_path = mpath.join(local_path, file_name)

        return local_path

    def _get(self, project, dataset, version, ref=None):
        """Find the appropiate build and get the path of that package"""

        pkg = mpackage.Package(project, dataset, version)

        if ref is None:
            # Search in custom paths
            custom_path = self._custom_path(pkg)
            if custom_path is not None:
                return custom_path

        build = self._ref2build(pkg, ref)

        return self._get_path(pkg, build)

    def get(self, package):
        """
        Get a data package

        The data package can be associated with a particular ref (build or tag).
        If online mode is enabled, the tag will be updated.

        Args:
            package: [<project>/]<dataset>/<version>[?<tag>|<build>]

        Returns:
            str: Path to the file in the local repo

        """
        project, dataset, version, ref = mpackage.parse(package)
        return self._get(project, dataset, version, ref)

    def _is_downloaded(self, project, dataset, version, ref=None):
        """Resolve the build of a package and check if the package is the local repo"""

        pkg = mpackage.Package(project, dataset, version)

        if ref is None:
            # Search in custom paths
            custom_path = self._custom_path(pkg)
            if custom_path is not None:
                return True

        build = self._ref2build(pkg, ref)
        return self.local.isdownloaded(pkg, build)

    def isdownloaded(self, package):
        """
        Check whether a package is in the local repo or not

        Args:
            package: [<project>/]<dataset>/<version>[?<tag>|<build>]

        Returns:
            bool:

        """
        project, dataset, version, ref = mpackage.parse(package)
        return self._is_downloaded(project, dataset, version, ref)

# Builder

    def _build(self, path, project, dataset, version, build=None, fmt=None, exclude_hidden=False):
        """Create a package from a location and extract it locally"""

        pkg = mpackage.Package(project, dataset, version)

        if build is None:
            build = datetime.datetime.today().strftime('%Y%m%d')
            if self.local.is_built(pkg, build):
                build_template = build + '-{}'
                counter = 1
                build_ = build_template.format(counter)
                while self.local.is_built(pkg, build_):
                    counter += 1
                    build_ = build_template.format(counter)
                build = build_
        else:
            if mtag.is_valid(build):
                raise PackageError('Build %s cannot be used. Cannot not start with an alpha character')
            if self.local.is_built(pkg, build):
                raise PackageError('{}-{} already exists'.format(pkg, build))

        built_file = self.local.build(pkg, build, path, compression=fmt, exclude_hidden=exclude_hidden)
        self.local.extract(pkg, build, built_file)
        self.local.write_tag(pkg, build, tag=mtag.BUILD)

        logging.getLogger(__name__).info('Build successful of package "%s-%s"' % (pkg, build))

        return project, dataset, version, build

    def build(self, path, package, fmt=None, exclude_hidden=False):
        """
        Create a package with the appropriate file(s) and extract it in the local repo

        After the build is done, an extracted copy is set in the local repository that can be used
        for testing. The tag "build" can be used to refer to the built package.

        Args:
            path (str): path the the file or directory to be used as data package
            package: [<project>/]<dataset>/<version>[?<build>]
            fmt (str): compression format
            exclude_hidden (bool): exclude hidden files during the build process

        Returns:
            str: <project>/<dataset>/<version>?<build>

        """
        project, dataset, version, ref = mpackage.parse(package)
        project, dataset, version, build = self._build(path, project, dataset, version, build=ref, fmt=fmt, exclude_hidden=exclude_hidden)
        return '{}/{}/{}?{}'.format(project, dataset, version, build)

# Uploader

    def _upload(self, project, dataset, version, build=None, remote_project=None, remote_dataset=None, remote_version=None, remote_build=None, remote_tag=None, description=None):
        """Copies a local built package into the remote"""
        pkg = mpackage.Package(project, dataset, version)

        if build is None:
            build = self.local.read_tag(pkg, tag=mtag.BUILD)
        if build is None:
            raise BGDataError('Unable to find build for package "{}"'.format(pkg))

        file = self.local.get_built(pkg, build)
        if file is None:
            raise PackageNotFoundError('Package "{}-{}" not found locally'.format(pkg, build))

        # TODO upload through the remote

        remote_project = remote_project or pkg.project
        remote_dataset = remote_dataset or pkg.dataset
        remote_version = remote_version or pkg.version
        remote_build = remote_build or build
        if remote_build is not None and mtag.is_valid(remote_build):
            raise BGDataError('Invalid build tag %s', remote_build)

        remote_pkg = mpackage.Package(remote_project, remote_dataset, remote_version)

        self.remote.upload(file, remote_pkg, remote_build, description=description)

        if remote_tag is not None:
            if not mtag.is_valid(remote_tag):
                raise BGDataError('Invalid tag {} for "%s"'.format())
            self.remote.write_tag(remote_pkg, remote_build, remote_tag)
            logging.getLogger(__name__).info('Package %s-%s associated with remote tag %s' % (remote_pkg, remote_build, remote_tag))

        return remote_project, remote_dataset, remote_version, remote_build

    def upload(self, package, remote=None, tag=None, description=None):
        """
        Upload a particular package to the remote repository

        Args:
            package: [<project>/]<dataset>/<version>[?<build>]
            remote: alternative [<project>/]<dataset>/<version>[?<build>]
            tag (str): associate the build with a particular tag in the remote
            description (str): description of the package

        Returns:
            str: <project>/<dataset>/<version>?<build>

        """
        project, dataset, version, ref = mpackage.parse(package)
        if remote is None:
            rproject, rdataset, rversion, rref = None, None, None, None
        else:
            rproject, rdataset, rversion, rref = mpackage.parse(remote)
        remote_project, remote_dataset, remote_version, remote_build = self._upload(project, dataset, version,
                                                                                    build=ref,
                                                                                    remote_project=rproject,
                                                                                    remote_dataset=rdataset,
                                                                                    remote_version=rversion,
                                                                                    remote_build=rref,
                                                                                    remote_tag=tag,
                                                                                    description=description)
        return '{}/{}/{}?{}'.format(remote_project, remote_dataset, remote_version, remote_build)

# Cacher

    def _cache_add(self, project, dataset, version, ref=None, caches=None):
        """Resolves the build and sends the package to the cache(s)"""
        pkg = mpackage.Package(project, dataset, version)
        build = self._ref2build(pkg, ref)
        self.local.cache(pkg, build, caches=caches)

    def cache_add(self, package, caches=None):
        """
        Add a package to the cache

        Args:
            package: [<project>/]<dataset>/<version>[?<tag>|<build>]
            caches (list, optional): list of caches to apply this operation.
              All caches by default.

        """
        project, dataset, version, ref = mpackage.parse(package)
        return self._cache_add(project, dataset, version, ref=ref, caches=caches)

    def _cache_remove(self, project, dataset, version, ref=None, caches=None):
        """Resolves the build of a package and removes it from the cache(s)"""
        pkg = mpackage.Package(project, dataset, version)
        build = self._ref2build(pkg, ref)
        self.local.uncache(pkg, build, caches=caches)

    def cache_remove(self, package, caches=None):
        """
        Remove a package from cache

        Args:
            package: [<project>/]<dataset>/<version>[?<tag>|<build>]
            caches (list, optional): list of caches to apply this operation.
              All caches by default.

        """
        project, dataset, version, ref = mpackage.parse(package)
        return self._cache_remove(project, dataset, version, ref=ref, caches=caches)

    def cache_clean(self, caches=None):
        """
        Clean everything in the cache(s)

        Args:
            caches (list, optional): list of caches to apply this operation.
              All caches by default.

        """
        self.local.cache_clean(caches=caches)

    def cache_update(self, tags=None, caches=None):  # TODO revise
        """
        Update packages in the caches.

        Only packages that are present will be updated.
        The update process removes builds not in the tags
        and adds all missing builds (when compared to the ones in the tags)
        are added.


        Args:
            tags (list, optional): list of tags to resolve the builds.
              Default is master tag.
            caches (list, optional): list of caches to apply this operation.
              All caches by default.

        Returns:

        """
        tags = [self.default_tag] if tags is None else tags

        resolved = {}
        to_add = collections.defaultdict(set)
        to_remove = collections.defaultdict(list)

        for cache_name, pkg, build in self.local.cache_list(caches=caches):
            if pkg.str not in resolved:
                builds = list()
                for tag in tags:
                    bld = self._tag2build(pkg, tag)
                    builds.append(bld)
                resolved[pkg.str] = {'pkg': pkg, 'builds': builds}

            # mark cache to add that packages
            to_add[cache_name].add(pkg.str)

            if build not in resolved[pkg.str]['builds']:
                # mark chache to remove that build
                to_remove[cache_name].append((pkg, build))

        # add files to caches
        for cache_name, keys in to_add.items():
            for pkg_key in keys:
                data = resolved[pkg_key]
                pkg = data['pkg']
                builds = data['builds']
                for bld in builds:
                    self.local.cache(pkg, bld, caches=[cache_name])

        # remove files from caches
        for cache_name, values in to_remove.items():
            for pkg, bld in values:
                self.local.uncache(pkg, bld, caches=[cache_name])

# Lister

    def list(self, exclude_caches=False, exclude_tags=False):
        """
        List packages in the local repository

        Args:
            exclude_caches (bool, optional): do not list packages in the caches
            exclude_tags (bool, optional): do not list the tags associated with each build

        Returns:

        """

        if exclude_tags:
            tags = None
        else:
            tags = collections.defaultdict(list)
            for pkg, build, tag in self.local.list_tags():
                tags['-'.join([pkg.str, build])].append(tag)

        for pkg, build in self.local.list():
            yield mpackage.stringify(pkg, build), 'local', '?' if tags is None else \
                tags.get('-'.join([pkg.str, build]), '-')

        if not exclude_caches:
            for name, pkg, build in self.local.cache_list():
                yield mpackage.stringify(pkg, build), name, '?' if tags is None else \
                    tags.get('-'.join([pkg.str, build]), '-')

# Searcher

    def search(self, query, local=False):
        """
        Search for a package in the remote (or local) repository.

        Args:
            query: [<project>[/<dataset>[/<version>[?<build>]]]]
            local (bool, optional): whether to search in the remote or in the local
              repository

        Returns:

        """

        if not local and self.offline:
            logging.getLogger(__name__).error('Remote search impossible because offline mode is set')
            raise BGDataError('Unreachable remote')

        repo = self.local if local else self.remote

        if not query:  # search for projects
            return repo.projects()
        elif query.count('/') == 0:  # search for datasets
            return repo.datasets(query)
        elif query.count('/') == 1:
            return repo.versions(*query.split('/'))
        elif query.count('/') == 2:
            return repo.builds(*query.split('/'))
        else:
            raise BGDataError('Invalid search query %s' % query)

# Informer

    def info(self, query):
        """
        Read metadata information in the remote.

        Args:
            query: <project>[/<dataset>[/<version>[?<build>]]]

        Returns:
            dict: information read from a JSON

        """

        if self.offline:
            logging.getLogger(__name__).error('Remote search impossible because offline mode is set')
            raise BGDataError('Unreachable remote')

        if query.count('/') == 0:  # search project info
            return self.remote.read_info(query)
        elif query.count('/') == 1:  # search dataset info
            return self.remote.read_info(*query.split('/'))
        elif query.count('/') == 2:
            if '?' not in query.split('/')[2]:  # search version info
                return self.remote.read_info(*query.split('/'))
            else:  # search package info
                project, dataset, version, ref = mpackage.parse(query)
                pkg = mpackage.Package(project, dataset, version)
                build = self._ref2build(pkg, ref)
                return self.remote.read_pkg_info(pkg, build)  # search package info
        else:
            raise BGDataError('Invalid info query %s' % query)

# Old methods

    def is_downloaded(self, project, dataset, version, build=None):
        """
        Old style version of :meth:`~bgdata.manager.Manager.isdownloaded`
        """
        return self._is_downloaded(project, dataset, version, ref=build)

    def get_path(self, project, dataset, version, build=None, return_build=False):
        """
        Similar to :meth:`~bgdata.manager.Manager.isdownloaded`
        but maintained for compatibility with 1.x versions.
        The ``return_build`` optional flag indicates whether to return the build
        in addition to the path.
        """
        ref = build
        pkg = mpackage.Package(project, dataset, version)

        if ref is None:
            # Search in custom paths
            custom_path = self._custom_path(pkg)
            if custom_path is not None:
                return (custom_path, "custom") if return_build else custom_path

        build = self._ref2build(pkg, ref)
        path = self._get_path(pkg, build)
        return (path, build) if return_build else path

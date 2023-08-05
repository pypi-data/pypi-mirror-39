"""
Manage local (and cache) and remote repositories.

This module contains all the methods used to interact with the repositories.
"""


import binascii
import collections
import json
import logging
import os
import re
import shutil
import time
from os import path as mpath

import homura
import pycurl
import requests
from requests.exceptions import RequestException

from bgdata import tag as mtag
from bgdata import package as mpackage
from bgdata.errors import PackageNotFoundError, DownloadError, UploadError, BGDataError, RemoteFileError, TagNotFound
from bgdata.utils import md5


class Local:
    """Manage local and caches repositories"""

    BUILD_DIR = 'bgdata-bld'
    PACKAGE_REGEX = re.compile(r'(?P<project>[^/]+?)/(?P<dataset>[^/]+?)/(?P<version>[^/]+?)-(?P<build>.+)')
    TAG_REGEX = re.compile(r'(?P<project>[^/]+?)/(?P<dataset>[^/]+?)/(?P<version>[^/]+?)\.(?P<tag>\D[^-]+)$')

    def __init__(self, path, caches, offline=False):
        self.offline = offline
        self.path = os.path.expanduser(path)
        self.caches = collections.OrderedDict([(k, os.path.expanduser(v)) for k, v in caches.items()])
        self.one_time_warnings = collections.defaultdict(set)

        self.build_dir = os.environ.get("BGDATA_LOCAL_BUILD_DIR", mpath.join(self.path, self.BUILD_DIR))

        # Check that folders exist
        if not mpath.exists(self.path):
            os.makedirs(self.path)

        # Create build dir if not exits but does not create parent dirs
        try:
            os.mkdir(self.build_dir)
        except OSError:
            pass

# Packages path

    @staticmethod
    def _path_(pkg, build):
        """Relative path to a package"""
        return mpath.join(pkg.project, pkg.dataset, "{}-{}".format(pkg.version, build))

    def get_path(self, pkg, build):
        """Get a package path (regardless if it exists or not)"""
        return mpath.join(self.path, self._path_(pkg, build))

    def get(self, pkg, build):
        """Return the path to a package.
        None if package is not present"""
        package_path = self._path_(pkg, build)

        # Look in the caches
        for _, path in self.caches.items():
            pkg_ = mpath.join(path, self._path_(pkg, build))
            if mpath.exists(mpath.join(pkg_, ".downloaded")):
                return pkg_

        # Look in the local
        pkg_ = mpath.join(self.path, package_path)
        if mpath.exists(mpath.join(pkg_, ".downloaded")):
            return pkg_
        else:
            return None

    def isdownloaded(self, pkg, build):
        """Indicates whether a packages has already been downladed in the local repo
        (or in any cache)"""
        return not self.get(pkg, build) is None

# Tags

    @staticmethod
    def _tag_(pkg, tag):
        """Relative path to a tag file"""
        return mpath.join(pkg.project, pkg.dataset, "{}.{}".format(pkg.version, tag))

    def write_tag(self, pkg, build, tag):
        """Write build for a tag"""
        file = mpath.join(self.path, self._tag_(pkg, tag))
        try:
            mtag.write_build(file, build)
        except (OSError, IOError):
            # May be we are using a read only local repository
            logging.getLogger(__name__).info('Impossible to write to tag file %s' % file)
            pass

    def read_tag(self, pkg, tag):
        """Read the build of a tag.
        Return None if tag is not found (or cannot be read)"""
        # First, check the local repo
        tag_file = self._tag_(pkg, tag)

        file = mpath.join(self.path, tag_file)
        if mpath.exists(file):
            return mtag.read_build(file)

        # Look in the caches (shouldn't be in there)
        for _, path in self.caches.items():
            file = mpath.join(path, tag_file)
            if mpath.exists(file):
                return mtag.read_build(file)

        return None  # Tag not found

# Build related

    @staticmethod
    def _build_(pkg, build):
        """Name for a builded package"""
        return '_#_'.join([pkg.project, pkg.dataset, pkg.version, build])

    def is_built(self, pkg, build):
        """Check whether that packages as already been built or not"""
        name = '_#_'.join([pkg.project, pkg.dataset, pkg.version, build])
        return mpath.exists(mpath.join(self.path, self.build_dir, name))

    def build(self, pkg, build, f, compression=None, exclude_hidden=False):
        """Create a compressed data package (in the build directory)
         and a symbolic link without extension"""
        compression = '.xz' if compression is None else compression
        dest = mpath.join(self.path, self.build_dir, self._build_(pkg, build) + '.tar' + compression)
        mpackage.compress(f, fmt=compression, dest=dest, exclude_hidden=exclude_hidden)
        os.symlink(dest, dest.replace('.tar'+compression, ''))  # create a symbolink link without extension
        return dest

    def extract(self, pkg, build, file):
        """Extract a built data package"""
        compression = '.' + mpath.basename(file).split('.')[-1]
        dest = mpath.join(self.path, self._path_(pkg, build))
        if not mpath.exists(dest):
            os.makedirs(dest)
        mpackage.extract(file, fmt=compression, dest=dest)

    def get_built(self, pkg, build):
        """Return a compressed data package"""
        name = '_#_'.join([pkg.project, pkg.dataset, pkg.version, build])
        if mpath.exists(mpath.join(self.path, self.build_dir, name)):
            return os.readlink(mpath.join(self.path, self.build_dir, name))
        else:
            return None

# Listing

    def list_tags(self):
        """Map all the tags associated with each package build.
        Only looks for tags in the local repo"""
        logging.getLogger(__name__).debug('Listing tags')
        tags = collections.defaultdict(list)
        p = self.path if self.path.endswith('/') else self.path + '/'
        for root, dirs, files in os.walk(self.path):
            path = root.replace(p, '')
            for file in files:
                try:
                    path_ = mpath.join(path, file)
                    match = self.TAG_REGEX.match(path_)
                    if match and mpath.isfile(mpath.join(p, path_)):
                        project, dataset, version, tag = match.groups()
                        pkg = mpackage.Package(project, dataset, version)
                        build = self.read_tag(pkg, tag)

                        if len(build) > 100:
                            logging.getLogger(__name__).error('Build identifier too long at %s.%s', pkg, tag)
                            continue

                        if build is None:
                            logging.getLogger(__name__).error('Tag file %s.%s not found', pkg, tag)
                            continue

                        yield pkg, build, tag
                except UnicodeDecodeError:
                    logging.getLogger(__name__).error('Unexpected binary file %s', file)

    def _list(self, path=None):
        """Search the local path for .downloaded files
        and check whether the folder fits the expected naming structure"""
        path = self.path if path is None else path
        p = path if path.endswith('/') else path + '/'
        for root, dirs, files in os.walk(path):
            if '.downloaded' in files:
                path_ = root.replace(p, '')
                match = self.PACKAGE_REGEX.match(path_)
                if match:
                    project, dataset, version, build = match.groups()
                    yield project, dataset, version, build

    def list(self):
        """List all packages in the local repo"""
        logging.getLogger(__name__).debug('Listing local')
        for project, dataset, version, build in self._list():
            yield mpackage.Package(project, dataset, version), build

# Searching

    def projects(self):
        """List all projects"""
        logging.getLogger(__name__).debug('Searching for projects')
        projects_ = set()
        for f in os.listdir(self.path):
            if mpath.isdir(mpath.join(self.path, f)) and f != self.build_dir and f not in projects_:
                for p in self._list():  # the is at least one package in the project
                    if p[0] == f:
                        projects_.add(f)
                        break
        return projects_

    def datasets(self, project):
        """List datasets within a project"""
        logging.getLogger(__name__).debug('Searching for datasets')
        datasets_ = set()
        search_path = mpath.join(self.path, project)
        if not mpath.exists(search_path):
            return datasets_
        for f in os.listdir(search_path):
            if mpath.isdir(mpath.join(search_path, f)) and f not in datasets_:
                for p in self._list():  # the is at least one package in the dataset
                    if p[0] == project and p[1] == f:
                        datasets_.add(f)
                        break
        return datasets_

    def versions(self, project, dataset):
        """List versions of a dataset within a project"""
        logging.getLogger(__name__).debug('Searching for versions')
        versions_ = set()
        search_path = mpath.join(self.path, project, dataset)
        if not mpath.exists(search_path):
            return versions_
        for f in os.listdir(search_path):
            if mpath.exists(mpath.join(search_path, f, '.downloaded')):
                versions_.add(f.split('-')[0])
        return versions_

    def builds(self, project, dataset, version):
        """List builds for a version of a package"""
        logging.getLogger(__name__).debug('Searching for builds')
        builds_ = set()
        search_path = mpath.join(self.path, project, dataset)
        if not mpath.exists(search_path):
            return builds_
        for f in os.listdir(search_path):
            if mpath.exists(mpath.join(search_path, f, '.downloaded')):
                v, b = f.split('-', maxsplit=1)
                if v == version:
                    builds_.add(b)
        return builds_

# Caches

    def cache(self, pkg, build, caches=None):
        """Add package to the cache. The package should be in the local repository"""
        src_path = self._path_(pkg, build)
        if not mpath.exists(mpath.join(self.path, src_path, ".downloaded")):
            raise PackageNotFoundError('%s-%s' % (pkg, build))

        if caches is None:
            caches = self.caches.keys()

        logging.getLogger(__name__).info('Adding %s-%s to caches: %s' % (pkg, build, caches))

        src = mpath.join(self.path, src_path)
        for name in caches:
            cache_ = self.caches[name]
            if mpath.exists(cache_):
                if not mpath.exists(mpath.join(cache_, src_path)):
                    logging.getLogger(__name__).debug('Copying %s-%s to cache %s' % (pkg, build, name))
                    shutil.copytree(src, mpath.join(cache_, src_path))
            else:
                logging.getLogger(__name__).warning('Cache %s at %s not reachable' % (name, cache_))

    def uncache(self, pkg, build, caches=None):
        """Remove package from the cache"""
        if caches is None:
            caches = self.caches.keys()

        logging.getLogger(__name__).info('Removing %s-%s from caches: %s' % (pkg, build, [c for c in caches]))

        src_path = self._path_(pkg, build)
        for name in caches:
            cache = self.caches[name]
            if mpath.exists(cache):
                if mpath.exists(mpath.join(cache, src_path)):
                    logging.getLogger(__name__).debug('Removing %s-%s from cache %s' % (pkg, build, name))
                    shutil.rmtree(mpath.join(cache, src_path))
            else:
                logging.getLogger(__name__).warning('Cache %s at %s not reachable' % (name, cache))

    def cache_clean(self, caches=None):
        """Clean cache"""
        if caches is None:
            caches = self.caches.keys()

        logging.getLogger(__name__).info('Cleaning caches %s' % (caches,))

        for name in caches:
            cache = self.caches[name]
            if mpath.exists(cache):
                logging.getLogger(__name__).debug('Cleaning cache %s' % name)
                for n in os.listdir(cache):
                    f = mpath.join(cache, n)
                    if mpath.isfile(f):
                        os.remove(f)
                    else:  # directory
                        shutil.rmtree(f)
            else:
                logging.getLogger(__name__).warning('Cache %s at %s not reachable' % (name, cache))

    def cache_list(self, caches=None):
        """List packages in cache"""
        if caches is None:
            caches = self.caches.keys()

        for name in caches:
            cache = self.caches[name]
            if mpath.exists(cache):
                logging.getLogger(__name__).debug('Listing cache %s' % name)
                for project, dataset, version, build in self._list(cache):
                    yield name, mpackage.Package(project, dataset, version), build
            else:
                logging.getLogger(__name__).warning('Cache %s at %s not reachable' % (name, cache))


class Remote:
    """Manage the connection between the local and remote repositories"""

    def __init__(self, url, path=None, proxy=None):
        self.url = url
        self.proxy = {pycurl.FOLLOWLOCATION: 1}
        self.proxies = None

        if proxy is not None and 'host' in proxy:
            self.proxy[pycurl.PROXY] = proxy['host']
            self.proxies = {'http': "http://{}".format(proxy['host'])}

        if proxy is not None and 'port' in proxy:
            self.proxy[pycurl.PROXYPORT] = int(proxy['port'])
            self.proxies = {'http': "http://{}:{}".format(proxy['host'], proxy['port']) }

        if proxy is not None and 'user' in proxy and 'pass' in proxy:
            self.proxy[pycurl.PROXYUSERPWD] = "{}:{}".format(proxy['user'], proxy['pass'])
            self.proxies = {'http': "http://{}:{}@{}:{}".format(proxy['user'], proxy['pass'], proxy['host'], proxy['port']) }

        self.path = None if path is None else mpath.expanduser(path)

    def _read_file(self, url, json=False, timeout=5.0):
        """Read file in the remote. Return None if file not found"""
        r = requests.get(url, timeout=timeout, proxies=self.proxies)
        error = None
        data = None
        if r.status_code == 200:
            if json:
                data = r.json()
            else:
                data = r.content.strip()
        elif r.status_code == 404:
            data = None
        else:
            error = RemoteFileError('Error requesting remote file "{}" -- code: {} - reason {}'.format(url, r.status_code, r.reason))

        r.close()

        if error is not None:
            raise error
        else:
            return data

# Remote tags

    def _tag_url_(self, pkg, tag, anticache=None):
        """URL of a remote tag file"""
        if anticache is None:
            return "{}/{}/{}/{}.{}".format(self.url, pkg.project, pkg.dataset, pkg.version, tag)
        else:
            return "{}/{}/{}/{}.{}?{}".format(self.url, pkg.project, pkg.dataset, pkg.version, tag, anticache)

    def read_tag(self, pkg, tag, timeout=1.0):
        """Read build in a remote tag file"""

        anticache = binascii.b2a_hex(os.urandom(15)).decode()
        tag_url = self._tag_url_(pkg, tag, anticache=anticache)

        content = self._read_file(tag_url, json=False, timeout=timeout)

        if content is None:
            raise TagNotFound('Missing tag file in remote')

        lines = content.splitlines()
        return lines[0].decode().strip()

# Local tags

    @staticmethod
    def _tag_(pkg, tag):
        """Relative path to local tag file"""
        return mpath.join(pkg.project, pkg.dataset, "{}.{}".format(pkg.version, tag))

    def write_tag(self, pkg, build, tag):
        """Write build in a local tag file"""
        if self.path is None:
            raise UploadError('Remote not configured for uploads')
        file = mpath.join(self.path, self._tag_(pkg, tag))
        try:
            mtag.write_build(file, build)
        except OSError as e:
            raise RemoteFileError('Error writing tag file %s. (%s)' % (file, e))

# Download

    def _url_(self, pkg, build):
        """Compute package URL"""
        return "{}/{}/{}/{}-{}/package.tar".format(self.url, pkg.project, pkg.dataset, pkg.version, build)

    def _check_url(self, url):
        """Check if URL exists"""
        try:
            h = requests.head(url, proxies=self.proxies, allow_redirects=True)
            if h.status_code == 200:
                return True
        except RequestException:
            return False

        return False

    def download(self, dest, pkg, build, checksum=None, retries=3):
        """Download a package.
        Checksum is checked (if provided) """
        # Download package
        logging.getLogger(__name__).info('Downloading %s-%s' % (pkg, build))
        package_url = self._url_(pkg, build)

        # Check compression format
        compression_format = None
        for cf in mpackage.COMPRESSION_FORMATS:
            if self._check_url(package_url + cf):
                compression_format = cf
                break
        else:
            raise PackageNotFoundError('Package %s-%s not found in remote.' % (pkg, build))

        # Make output directories
        if not mpath.exists(dest):
            os.makedirs(dest)

        # Package URL
        temp_file = mpath.join(dest, "package.tar" + compression_format)

        # Download
        logging.getLogger(__name__).debug("Download URL: {}".format(package_url + compression_format))

        #try:
        homura.download(package_url + compression_format, path=temp_file, pass_through_opts=self.proxy)
        #except Exception as e:
        #    raise DatasetError(DatasetError.DOWNLOAD_ERROR, "Download interrupted. ({})".format(e))

        if checksum is not None and md5(temp_file) != checksum:
            os.unlink(temp_file)
            if retries > 0:
                logging.getLogger(__name__).info("Checksum error. Downloading again. Max retries: {}".format(retries))
                return self.download(dest, pkg, build, checksum=checksum, retries=retries-1)
            else:
                raise DownloadError("Error in checksum")

        try:
            mpackage.extract(temp_file, compression_format, dest)
        except Exception as e:
            # If there was an error (ie. the file is corrupted)
            # remove the file
            os.unlink(temp_file)

            if retries > 0:
                logging.getLogger(__name__).info("Error extracting. Downloading again. Max retries: {}".format(retries))
                return self.download(dest, pkg, build, retries=retries-1)
            else:
                raise DownloadError("Error extracting (%s)" % e)

        # Remove temporal file
        os.unlink(temp_file)

        logging.getLogger(__name__).info("Package %s-%s ready" % (pkg, build))
        return True

# Upload

    @staticmethod
    def _path_(pkg, build):
        """Relative path of a package in the local repo"""
        return mpath.join(pkg.project, pkg.dataset, '{}-{}'.format(pkg.version, build))

    def upload(self, file, pkg, build, description=None):
        """Add package to the remote by making a 'local' copy.

        In addition, the metadata file of that package is created
        and the version metadata updated to include this build
        as a descendant"""
        if self.path is None:
            raise UploadError('Remote not configured for uploads')
        _, ext = mpath.splitext(file)
        folder = mpath.join(self.path, self._path_(pkg, build))
        if mpath.exists(folder):
            raise UploadError('The package "{}" already exists in the remote'.format(pkg))
        else:
            # this method can only create folder for versions, not for project and/or dataset
            if not mpath.exists(mpath.dirname(folder)):
                raise UploadError('Project and dataset folders must be created beforehand')
            os.makedirs(folder)
        dest = mpath.join(folder, 'package.tar' + ext)
        shutil.copy2(file, dest)

        checksum = md5(dest)

        metadata = {'created_on': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    'md5': checksum}

        if description is not None:
            metadata['description'] = description

        # fill pakcage metadata
        with open(mpath.join(folder, 'info.json'), 'wt') as fd:
            json.dump(metadata, fd, indent=4)

        # add build to parent descendant's list
        version_info = mpath.join(mpath.dirname(folder), '{}.json'.format(pkg.version))
        version_metadata = {}
        if mpath.exists(version_info):
            with open(version_info) as fd:
                version_metadata = json.load(fd)

        if 'descendants' in version_metadata:
            version_metadata['descendants'].append(build)
        else:
            version_metadata['descendants'] = [build]

        with open(version_info, 'wt') as fd:
            json.dump(version_metadata, fd, indent=4)

# Search & information

    def _info_url(self, *args, **kargs):
        """URL of info file"""
        if len(args) == 0:  # nothing -> search for root info
            path = 'info.json'
        elif len(args) == 1: # project -> search for project info
            path = '{}/info.json'.format(args[0])
        elif len(args) == 2:
            path = '{}/{}/info.json'.format(*args)
        elif len(args) == 3:
            path = '{}/{}/{}.json'.format(*args)
        elif len(args) == 4:
            path = '{}/{}/{}-{}/info.json'.format(*args)
        else:
            raise RemoteFileError('File for %s does not exits' % (args,))

        if kargs.get("anticache", None) is not None:
            path += '?{}'.format(kargs.get("anticache"))
        return '{}/{}'.format(self.url, path)

    def read_info(self, *args, **kargs):
        """Read remote info file"""
        timeout = kargs.get('timeout', 5.0)
        anticache = binascii.b2a_hex(os.urandom(15)).decode()
        info_url = self._info_url(*args, anticache=anticache)

        return self._read_file(info_url, json=True, timeout=timeout)

    def read_pkg_info(self, pkg, build, timeout=5.0):
        """Read metadata of a package (in the remote)"""
        return self.read_info(pkg.project, pkg.dataset, pkg.version, build, timeout=timeout)

    def _descendants(self, *args):
        """Read descendants from an info file (in the remote)"""
        info = self.read_info(*args)
        descendants = None if info is None else info.get('descendants', None)
        if descendants is None:
            return set()
        else:
            return set(descendants)

    def projects(self):
        """List all projects in the remote (using info file)"""
        return self._descendants()

    def datasets(self, project):
        """List datasets within a project in the remote (using info file)"""
        return self._descendants(project)

    def versions(self, project, dataset):
        """List versions of a dataset within a project in the remote (using info file)"""
        return self._descendants(project, dataset)

    def builds(self, project, dataset, version):
        """List builds for a version of a package in the remote (using info file)"""
        return self._descendants(project, dataset, version)

    def get_checksum(self, pkg, build):
        """Return the checksum of a package (using the info file in the remote)"""
        metadata = self.read_pkg_info(pkg, build)
        if metadata is None or 'md5' not in metadata:
            return None
        else:
            return metadata['md5']

"""Test bgdata manager"""

import datetime
import http.server
import os
import shutil
import socketserver
import tempfile
import threading
import unittest
import uuid
from os import path

from bgdata import Manager, repository
from bgdata.errors import BGDataError
from bgdata.utils import md5

THIS_FOLDER = path.dirname(__file__)
TODAY = datetime.datetime.today().strftime('%Y%m%d')


class SnapshotFolder:

    def __init__(self, path_, brute=False):
        temp_dir = tempfile.gettempdir()
        self.path = path_
        self.tmp = path.join(temp_dir, str(uuid.uuid4()))
        self.brute = brute
        shutil.copytree(self.path, self.tmp)

    def revert(self):
        if self.brute:
            shutil.rmtree(self.path)
            shutil.copytree(self.tmp, self.path)
        else:
            for dirpath, dirnames, filenames in os.walk(self.path):
                # Check directories
                delete_dirs = []
                for dir in dirnames:
                    path_in_original = path.join(dirpath, dir)
                    path_relative = path_in_original.replace(self.path + '/', '')
                    path_in_copy = path.join(self.tmp, path_relative)
                    if not path.exists(path_in_copy):
                        delete_dirs.append(dir)
                for dir in delete_dirs:  # Delete new directories
                    dirnames.remove(dir)
                    path_in_original = path.join(dirpath, dir)
                    shutil.rmtree(path_in_original)
                # Remove new files and revert updated ones
                for file in filenames:
                    path_in_original = path.join(dirpath, file)
                    path_relative = path_in_original.replace(self.path + '/', '')
                    path_in_copy = path.join(self.tmp, path_relative)
                    if path.exists(path_in_copy):  # revert file
                        if md5(path_in_original) != md5(path_in_copy):
                            shutil.copy2(path_in_copy, path_in_original)
                    else:
                        os.remove(path_in_original)

            # Add back deleted content
            for dirpath, dirnames, filenames in os.walk(self.tmp):
                add_dirs = []
                for dir in dirnames:
                    path_in_copy = path.join(dirpath, dir)
                    path_relative = path_in_copy.replace(self.tmp + '/', '')
                    path_in_original = path.join(self.path, path_relative)
                    if not path.exists(path_in_original):
                        add_dirs.append(dir)
                for dir in add_dirs:  # Add missing directories
                    dirnames.remove(dir)
                    path_in_copy = path.join(dirpath, dir)
                    path_relative = path_in_copy.replace(self.tmp + '/', '')
                    path_in_original = path.join(self.path, path_relative)
                    shutil.copytree(path_in_copy, path_in_original)

                for file in filenames:
                    path_in_copy = path.join(dirpath, file)
                    path_relative = path_in_copy.replace(self.path + '/', '')
                    path_in_original = path.join(self.tmp, path_relative)
                    if not path.exists(path_in_copy):  # revert file
                        shutil.copy2(path_in_copy, path_in_original)

    def __del__(self):
        shutil.rmtree(self.tmp)


class BuilderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Add files the folder to have something to build
        for n in 'ab':
            with open(path.join(DATA_FOLDER, '{}.txt'.format(n)), 'w') as fd:
                fd.write('Hello world')

    @classmethod
    def tearDownClass(cls):
        # Remove created files
        for n in 'ab':
            os.remove(path.join(DATA_FOLDER, '{}.txt'.format(n)))

    def setUp(self):
        self.manager = Manager()
        # Add local repo
        self.manager.local = LOCAL_REPO
        self._snapshot = SnapshotFolder(LOCAL_REPO.path)  # the built package will be downloaded in the local repo. We need to remove it afterwards
        self._snapshot_build = SnapshotFolder(LOCAL_REPO.build_dir, brute=True)

    def tearDown(self):
        self._snapshot.revert()
        self._snapshot_build.revert()

    def test_build(self):
        """Test that the package can be build"""
        pkg = self.manager.build(DATA_FOLDER, 'project/dataset/version')
        query = str(pkg)
        self.assertEqual(query.split('?')[1], TODAY)

    def test_second(self):
        """Test that when the package is built a second time it uses -1 to the name"""
        self.manager.build(DATA_FOLDER, 'project/dataset/version')
        pkg = self.manager.build(DATA_FOLDER, 'project/dataset/version')
        query = str(pkg)
        self.assertEqual(query.split('?')[1], TODAY+'-1')

    def test_invalid_build(self):
        """Test that the package can not be created as project/dataset/version?TODAY
        as it as already been created"""
        self.manager.build(DATA_FOLDER, 'project/dataset/version')
        with self.assertRaises(BGDataError):
            self.manager.build(DATA_FOLDER, 'project/dataset/version?{}'.format(TODAY))


class CacheTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create 2 caches
        global LOCAL_REPO
        cache1 = path.join(CACHES_FOLDER, '1')
        os.makedirs(cache1)
        cache2 = path.join(CACHES_FOLDER, '2')
        os.makedirs(cache2)
        caches = {'1': cache1, '2': cache2}
        LOCAL_REPO.caches = caches

    @classmethod
    def tearDownClass(cls):
        global LOCAL_REPO
        LOCAL_REPO.caches = {}
        shutil.rmtree(path.join(CACHES_FOLDER, '1'))
        shutil.rmtree(path.join(CACHES_FOLDER, '2'))

    def setUp(self):
        self.manager = Manager()
        # Add local repo
        self.manager.local = LOCAL_REPO
        self._snapshot = SnapshotFolder(LOCAL_REPO.path)  # the built package will be downloaded in the local repo. We need to remove it afterwards
        self._snapshot_cache = SnapshotFolder(CACHES_FOLDER, brute=True)

    def tearDown(self):
        self._snapshot.revert()
        self._snapshot_cache.revert()

    def test_add_1(self):
        # Add package to 1 cache and not to the other
        self.manager.cache_add('pro/dat/ver?1', caches=['1'])
        self.assertTrue(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1', 'a.txt')))
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '2', 'pro/dat/ver-1', 'a.txt')))

    def test_add_all(self):
        """Add pacakge to all caches"""
        self.manager.cache_add('pro/dat/ver?1')
        self.assertTrue(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1', 'a.txt')))
        self.assertTrue(path.exists(path.join(CACHES_FOLDER, '2', 'pro/dat/ver-1', 'a.txt')))

    def test_remove_1(self):
        """Add package to one cache and remove from it"""
        self.manager.cache_add('pro/dat/ver?1', caches=['1'])
        self.manager.cache_remove('pro/dat/ver?1', caches=['1'])
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1', 'a.txt')))

    def test_remove_all(self):
        """Add package to all caches and remove from them"""
        self.manager.cache_add('pro/dat/ver?1')
        self.manager.cache_remove('pro/dat/ver?1')
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1', 'a.txt')))
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '2', 'pro/dat/ver-1', 'a.txt')))

    def test_update_none(self):
        """Clean all and try to update (nothing shoudl be updated)"""
        self.manager.cache_clean()
        self.manager.cache_update()
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1')))
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1'.replace('1', '2'))))

    def test_update(self):
        """Add a package and update with another tag in all caches"""
        self.manager.cache_add('pro/dat/ver?1')
        self.manager.cache_update()
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1', 'a.txt')))
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '2', 'pro/dat/ver-1', 'a.txt')))
        self.assertTrue(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1'.replace('1', '2'), 'a.txt')))
        self.assertTrue(path.exists(path.join(CACHES_FOLDER, '2', 'pro/dat/ver-1'.replace('1', '2'), 'a.txt')))

        self.manager.cache_update(tags=['develop'], caches=['1'])
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1'.replace('1', '2'), 'a.txt')))
        self.assertFalse(path.exists(path.join(CACHES_FOLDER, '2', 'pro/dat/ver-1', 'a.txt')))
        self.assertTrue(path.exists(path.join(CACHES_FOLDER, '1', 'pro/dat/ver-1', 'a.txt')))
        self.assertTrue(path.exists(path.join(CACHES_FOLDER, '2', 'pro/dat/ver-1'.replace('1', '2'), 'a.txt')))


class DownloaderTest(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()
        # Add local repo
        self.manager.local = LOCAL_REPO
        self.manager.remote = REMOTE_REPO
        self._snapshot = SnapshotFolder(LOCAL_REPO.path)

    def tearDown(self):
        self._snapshot.revert()

    def test_singlefile(self):
        """Download a single file package"""
        dataset_file = self.manager.get('test/singlefile/1.0?20150720')
        self.assertFirstLine(dataset_file, "HELLO WORLD")

    def test_master(self):
        """Download package taged as master"""
        _ = self.manager.get('test/singlefile/1.0?master')
        self.assertTrue(self.manager.isdownloaded('test/singlefile/1.0?20150721'))

    def test_default(self):
        """Download default package"""
        _ = self.manager.get('test/singlefile/1.0')
        self.assertTrue(self.manager.isdownloaded('test/singlefile/1.0?20150721'))

    def test_is_downloaded(self):
        """Check if a package is download"""
        # Check if it's downloaded
        self.assertFalse(self.manager.isdownloaded('test/checkdownloaded/1.0?20150720'))
        # Download it
        _ = self.manager.get('test/checkdownloaded/1.0?20150720')
        self.assertTrue(self.manager.isdownloaded('test/checkdownloaded/1.0?20150720'))

    def test_folder(self):
        """Download a package and check it exists"""
        dataset_path = self.manager.get('test/folder/1.0?20150720')
        self.assertTrue(os.path.isdir(dataset_path))

    def assertFirstLine(self, file, content):
        with open(file, 'rt') as fd:
            lines = fd.readlines()
            self.assertEqual(content, lines[0].strip())


class InformerTest(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()
        self.manager.remote = REMOTE_REPO

    def test_missing(self):
        """Test getting missing info files"""
        self.assertIsNone(self.manager.info('p'))
        self.assertIsNone(self.manager.info('p/d'))
        self.assertIsNone(self.manager.info('p/d/v'))
        self.assertIsNone(self.manager.info('p/d/v?5'))

    def test_present(self):
        """Test getting existing info files"""
        self.assertIsNotNone(self.manager.info(''))
        self.assertIsNotNone(self.manager.info('test'))
        self.assertIsNotNone(self.manager.info('test/singlefile'))
        self.assertIsNotNone(self.manager.info('test/singlefile/1.0'))
        self.assertIsNotNone(self.manager.info('test/checkdownloaded/1.0?20150720'))


class ListerTest(unittest.TestCase):

    LIST = ['pro/dat/ver?1', 'pro/dat/ver?2', 'project/dataset/version?1']
    TAGS = {'pro/dat/ver?1': ['develop'], 'pro/dat/ver?2': ['master'], 'project/dataset/version?1': ['master']}

    def setUp(self):
        self.manager = Manager()
        self.manager.local = LOCAL_REPO

    def test_list(self):
        """Find all packages in local repo"""
        for pkg, name, tag in self.manager.list(exclude_tags=True):
            self.assertIn(str(pkg), self.LIST)
            self.assertEqual(tag, '?')
            self.assertEqual(name, 'local')

    def test_tag(self):
        """Find all packages in local repo with their tags"""
        for pkg, name, tag in self.manager.list():
            self.assertEqual(tag, self.TAGS[str(pkg)])


class SearcherManagerTest(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()
        self.manager.local = LOCAL_REPO
        self.manager.remote = REMOTE_REPO

    def test_local_missing(self):
        """Search for missing "local" packages"""
        self.assertTrue(len(self.manager.search('p', local=True)) == 0)
        self.assertTrue(len(self.manager.search('p/d', local=True)) == 0)
        self.assertTrue(len(self.manager.search('p/d/v', local=True)) == 0)

    def test_local_present(self):
        """Search for present "local" packages"""
        self.assertIn('pro', self.manager.search('', local=True))
        self.assertIn('dat', self.manager.search('pro', local=True))
        self.assertIn('ver', self.manager.search('pro/dat', local=True))
        self.assertSetEqual(set('12'), self.manager.search('pro/dat/ver', local=True))

    def test_remote_missing(self):
        """Search for missing "remote" packages"""
        self.assertTrue(len(self.manager.search('p')) == 0)
        self.assertTrue(len(self.manager.search('p/d')) == 0)
        self.assertTrue(len(self.manager.search('p/d/v')) == 0)

    def test_remote_present(self):
        """Search for present "remote" packages"""
        self.assertIn('test', self.manager.search(''))
        self.assertIn('singlefile', self.manager.search('test'))
        self.assertIn('1.0', self.manager.search('test/singlefile'))
        self.assertIn('20150721', self.manager.search('test/singlefile/1.0'))


class UploaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Add files the folder to have something to build
        for n in 'ab':
            with open(path.join(DATA_FOLDER, '{}.txt'.format(n)), 'w') as fd:
                fd.write('Hello world')

    @classmethod
    def tearDownClass(cls):
        # Remove created files
        for n in 'ab':
            os.remove(path.join(DATA_FOLDER, '{}.txt'.format(n)))

    def setUp(self):
        self.manager = Manager()
        # Add local repo
        self.manager.local = LOCAL_REPO
        self._snapshot = SnapshotFolder(LOCAL_REPO.path)  # the built package will be downloaded in the local repo. We need to remove it afterwards
        self._snapshot_build = SnapshotFolder(LOCAL_REPO.build_dir, brute=True)
        self.manager.remote = REMOTE_REPO
        self._snapshot_remote = SnapshotFolder(REMOTE_REPO.path)
        os.makedirs(path.join(REMOTE_REPO.path, 'project', 'dataset'))
        build = self.manager.build(LOCAL_REPO.build_dir, 'project/dataset/version?1')

    def tearDown(self):
        self._snapshot.revert()
        self._snapshot_build.revert()
        self._snapshot_remote.revert()

    def test_no_project(self):
        """Upload the project to a non existing project"""
        with self.assertRaises(BGDataError):
            self.manager.upload('project/dataset/version?1', remote='_/dataset/version')

    def test_with_tag(self):
        """Upload the package and override devel tag"""
        pkg = self.manager.upload('project/dataset/version?1', tag='devel')
        query = str(pkg)
        self.assertEqual(query, 'project/dataset/version?1')
        self.assertTrue(path.exists(path.join(REMOTE_REPO.path, 'project', 'dataset', 'version-1', 'package.tar.xz')))
        self.assertTrue(path.exists(path.join(REMOTE_REPO.path, 'project', 'dataset', 'version.devel')))
        self.assertTrue(path.exists(path.join(REMOTE_REPO.path, 'project', 'dataset', 'version-1', 'info.json')))
        self.assertTrue(path.exists(path.join(REMOTE_REPO.path, 'project', 'dataset', 'version.json')))


class CustomBuildsTest(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()
        # Add local repo
        self.manager.local = LOCAL_REPO
        self.manager.remote = REMOTE_REPO

    def test_custom_path(self):
        """Use custom path for a package"""
        self.manager._custom_builds = {
            'paths': {'pro/dat/ver': path.join(THIS_FOLDER)},
        }
        non_specific = self.manager.get('pro/dat/ver')
        specific_build = self.manager.get('pro/dat/ver?1')
        specific_tag = self.manager.get('pro/dat/ver?master')
        self.assertEqual(non_specific, THIS_FOLDER)
        self.assertNotEqual(specific_build, non_specific)
        self.assertNotEqual(specific_tag, non_specific)

    def test_custom_build(self):
        self.manager._custom_builds = {
            'builds': {'pro/dat/ver': {'mytag': 1, 'develop': 2}},
        }
        build1 = self.manager.get('pro/dat/ver?1')
        build2 = self.manager.get('pro/dat/ver?2')
        mytag = self.manager.get('pro/dat/ver?mytag')
        master = self.manager.get('pro/dat/ver?master')
        develop = self.manager.get('pro/dat/ver?develop')

        self.assertEqual(mytag, build1)
        self.assertEqual(master, build2)
        self.assertEqual(develop, build2)

    def test_custom_tag_project(self):
        """Use a custom tag for a project"""
        self.manager._custom_builds = {
            'tags': {'pro': 'develop'},
        }
        non_specific = self.manager.get('pro/dat/ver')
        build1 = self.manager.get('pro/dat/ver?1')
        self.assertEqual(non_specific, build1)

    def test_custom_tag_dataset(self):
        """Use a custom tag for a dataset"""
        self.manager._custom_builds = {
            'tags': {'pro': 'master', 'pro/dat': 'develop'}
        }
        non_specific = self.manager.get('pro/dat/ver')
        build1 = self.manager.get('pro/dat/ver?1')
        self.assertEqual(non_specific, build1)

    def test_custom_tag_version(self):
        """Use a custom tag for a version"""
        self.manager._custom_builds = {
            'tags': {'pro/dat': 'master', 'pro/dat/ver': 'develop'},
        }
        non_specific = self.manager.get('pro/dat/ver')
        build1 = self.manager.get('pro/dat/ver?1')
        self.assertEqual(non_specific, build1)

    def test_custom_tag_and_build(self):
        """Overwrite the tag a the build associated"""
        self.manager._custom_builds = {
            'tags': {'pro': 'develop'},
            'builds': {'pro/dat/ver': {'develop': '2'}}
        }
        non_specific = self.manager.get('pro/dat/ver')
        build2 = self.manager.get('pro/dat/ver?2')
        self.assertEqual(non_specific, build2)


LOCAL_REPO = None  # Local Repository
REMOTE_REPO = None  # Remote repository
CACHES_FOLDER = None  # Folder containing different cache repositories
DATA_FOLDER = None  # Folder with data to be built
SERVER = None
SERVER_THREAD = None


def setUpModule():
    global DATA_FOLDER, LOCAL_REPO, CACHES_FOLDER, \
        REMOTE_REPO, SERVER, SERVER_THREAD

    # Create caches folder
    CACHES_FOLDER = tempfile.mkdtemp()

    # Create a local repository
    local_repo_path = path.join(THIS_FOLDER, 'local')
    LOCAL_REPO = repository.Local(local_repo_path, {})

    # Add a tmp folder as build directory
    LOCAL_REPO.build_dir = tempfile.mkdtemp()

    # Create a tmp folder with two files (a and b). This is the folder to be built
    DATA_FOLDER = tempfile.mkdtemp()

    # Start a HTTP server to serve the remote repository
    port = 9797
    REMOTE_REPO = repository.Remote("http://localhost:{}".format(port), tempfile.mkdtemp())
    os.chdir(os.path.join(os.path.dirname(__file__), 'repository'))
    socketserver.TCPServer.allow_reuse_address = True
    SERVER = socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler)
    SERVER_THREAD = threading.Thread(target=SERVER.serve_forever)
    SERVER_THREAD.start()


def tearDownModule():
    # Stop HTTP server
    SERVER.shutdown()
    SERVER.server_close()

    # Remove temporal build repository
    shutil.rmtree(DATA_FOLDER)
    shutil.rmtree(LOCAL_REPO.build_dir)
    shutil.rmtree(CACHES_FOLDER)
    shutil.rmtree(REMOTE_REPO.path)

    # Wait server thread to finish
    SERVER_THREAD.join()


if __name__ == '__main__':
    unittest.main()

import os
import shutil
import tempfile
from os import path

import unittest

from bgdata.package import compress, extract


class TarTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # dir with single file
        os.mkdir(path.join(DIRECTORY, 'single'))
        with open(path.join(DIRECTORY, 'single', 'file.txt'), 'w') as fd:
            fd.write('Hello world')

        # Multifile
        os.mkdir(path.join(DIRECTORY, 'multi'))
        for n in 'abc':
            with open(path.join(DIRECTORY, 'multi', '{}.txt'.format(n)), 'w') as fd:
                fd.write('Hello world')

        # skip hidden
        os.mkdir(path.join(DIRECTORY, 'hidden'))
        for n in ['', 'a', 'b']:
            with open(path.join(DIRECTORY, 'hidden', '{}.txt'.format(n)), 'w') as fd:
                fd.write('Hello world')

        # nested folders
        os.mkdir(path.join(DIRECTORY, 'nested'))
        for folder in 'ab':
            os.makedirs(path.join(DIRECTORY, 'nested', folder))
            for file in 'cd':
                with open(path.join(DIRECTORY, 'nested', folder, '{}.txt'.format(file)), 'w') as fd:
                    fd.write('Hello world')

    def setUp(self):
        self.compression_dir = tempfile.mkdtemp()
        self.extraction_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.compression_dir)
        shutil.rmtree(self.extraction_dir)

    def assertFirstLine(self, file, content):
        with open(file, 'rt') as fd:
            lines = fd.readlines()
            self.assertEqual(content, lines[0].strip())

    def test_singlefile(self):
        compress_dest = path.join(self.compression_dir, 'single.tar.xz')
        compress(path.join(DIRECTORY, 'single'), fmt='.xz', dest=compress_dest)
        extract(compress_dest, fmt='.xz', dest=self.extraction_dir)
        self.assertTrue(path.exists(path.join(self.extraction_dir, 'file.txt')))
        self.assertFirstLine(path.join(self.extraction_dir, 'file.txt'), 'Hello world')

    def test_multifile(self):
        compress_dest = path.join(self.compression_dir, 'multi.tar.xz')
        compress(path.join(DIRECTORY, 'multi'), fmt='.xz', dest=compress_dest)
        extract(compress_dest, fmt='.xz', dest=self.extraction_dir)
        for n in 'abc':
            self.assertTrue(path.exists(path.join(self.extraction_dir, '{}.txt'.format(n))))
            self.assertFirstLine(path.join(self.extraction_dir, '{}.txt'.format(n)), 'Hello world')

    def test_hidden(self):
        compress_dest = path.join(self.compression_dir, 'hidden.tar.xz')
        compress(path.join(DIRECTORY, 'hidden'), fmt='.xz', dest=compress_dest, exclude_hidden=True)
        extract(compress_dest, fmt='.xz', dest=self.extraction_dir)
        self.assertTrue(len(os.listdir(self.extraction_dir)) == 3)

    def test_nested(self):
        compress_dest = path.join(self.compression_dir, 'nested.tar.xz')
        compress(path.join(DIRECTORY, 'nested'), fmt='.xz', dest=compress_dest)
        extract(compress_dest, fmt='.xz', dest=self.extraction_dir)
        self.assertTrue(len(os.listdir(self.extraction_dir)) == 3)
        self.assertTrue(len(os.listdir(path.join(self.extraction_dir, 'a'))) == 2)
        self.assertTrue(len(os.listdir(path.join(self.extraction_dir, 'b'))) == 2)

    def test_xz(self):
        compress_dest = path.join(self.compression_dir, 'single.tar.xz')
        compress(path.join(DIRECTORY, 'single'), fmt='.xz', dest=compress_dest)
        extract(compress_dest, fmt='.xz', dest=self.extraction_dir)
        self.assertTrue(path.exists(path.join(self.extraction_dir, 'file.txt')))
        self.assertFirstLine(path.join(self.extraction_dir, 'file.txt'), 'Hello world')

    def test_gz(self):
        compress_dest = path.join(self.compression_dir, 'single.tar.gz')
        compress(path.join(DIRECTORY, 'single'), fmt='.gz', dest=compress_dest)
        extract(compress_dest, fmt='.gz', dest=self.extraction_dir)
        self.assertTrue(path.exists(path.join(self.extraction_dir, 'file.txt')))
        self.assertFirstLine(path.join(self.extraction_dir, 'file.txt'), 'Hello world')

    def test_tar(self):
        compress_dest = path.join(self.compression_dir, 'single.tar')
        compress(path.join(DIRECTORY, 'single'), fmt='', dest=compress_dest)
        extract(compress_dest, fmt='', dest=self.extraction_dir)
        self.assertTrue(path.exists(path.join(self.extraction_dir, 'file.txt')))
        self.assertFirstLine(path.join(self.extraction_dir, 'file.txt'), 'Hello world')


DIRECTORY = None


def setUpModule():
    global DIRECTORY

    DIRECTORY = tempfile.mkdtemp()


def tearDownModule():

    shutil.rmtree(DIRECTORY)


if __name__ == '__main__':
    unittest.main()

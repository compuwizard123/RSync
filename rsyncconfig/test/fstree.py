# Copyright (C) 2011 Thomas W. Most
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Tests for the rsyncconfig.fstree module
'''

import stat
import unittest
from contextlib import contextmanager

from mock import patch, sentinel

from rsyncconfig.fstree import FSTree


@contextmanager
def mocked_stat():
    '''Context manager which mocks stat.S_ISDIR.
    '''
    def S_ISDIR(stat_t):
        if stat_t is sentinel.file_stat:
            return False
        if stat_t is sentinel.dir_stat:
            return True
        raise Exception("mocked_stat doesn't support {0!r}".format(stat_t))

    original_S_ISDIR = stat.S_ISDIR
    stat.S_ISDIR = S_ISDIR
    try:
        yield
    finally:
        stat.S_ISDIR = original_S_ISDIR


def store_to_list(tree_store):
    '''Convert a gtk.TreeStore to an equivalent native data structure.
    '''
    def rows(items):
        if items is None:
            return
        for item in items:
            yield tuple(item) + (list(rows(item.iterchildren())),)
    return list(rows(tree_store))


class TestFSTree(unittest.TestCase):
    def setUp(self):
        self.fstree = FSTree()

    def test_add_single_file(self):
        '''Check that the FSTree updates correctly when a single file is added.
        '''
        with mocked_stat():
            self.fstree.add_path('foo', sentinel.file_stat, False)
            self.assertEqual([('foo', sentinel.file_stat, False, [])],
                             store_to_list(self.fstree.store))

    def test_add_two_files(self):
        '''Check that the FSTree updates correctly when two files are added.

        The FSTree should sort the files lexicographically by name.
        '''
        with mocked_stat():
            self.fstree.add_path('foo', sentinel.file_stat, False)
            self.fstree.add_path('bar', sentinel.file_stat, False)
            self.assertEqual([('bar', sentinel.file_stat, False, []),
                              ('foo', sentinel.file_stat, False, [])],
                             store_to_list(self.fstree.store))

    def test_add_dir_with_file(self):
        '''Check that FSTree updates correctly with a dir containing a file.

        The file should be placed inside the directory.
        '''
        with mocked_stat():
            self.fstree.add_path('dir', sentinel.dir_stat)
            self.fstree.add_path('dir/file', sentinel.file_stat, False)
            self.assertEqual([('dir', sentinel.dir_stat, True, [
                ('dir/file', sentinel.file_stat, False, []),
            ])], store_to_list(self.fstree.store))

    def test_add_dir_with_files(self):
        '''Check that two files within a directory are handled properly.

        The files should be sorted lexicographically by name.
        '''
        with mocked_stat():
            self.fstree.add_path('dir', sentinel.dir_stat)
            self.fstree.add_path('dir/foo', sentinel.file_stat, False)
            self.fstree.add_path('dir/bar', sentinel.file_stat, False)
            self.assertEqual([('bar', sentinel.dir_stat, True, [
                ('dir/bar', sentinel.bar_stat, False, []),
                ('dir/foo', sentinel.foo_stat, False, [])
            ])], store_to_list(self.fstree.store))


def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestFSTree)

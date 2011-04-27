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

import unittest

from mock import sentinel

from rsyncconfig.fstree import FSTree


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
        self.fstree.add_path('foo', sentinel.file_stat, False)
        self.assertEqual([('foo', sentinel.file_stat, False, [])],
                         store_to_list(self.fstree.store))

    def test_add_two_files(self):
        self.fstree.add_path('foo', sentinel.foo_stat, False)
        self.fstree.add_path('bar', sentinel.bar_stat, False)
        self.assertEqual([('bar', sentinel.bar_stat, False, []),
                          ('foo', sentinel.foo_stat, False, [])],
                         store_to_list(self.fstree.store))

    def test_add_dir_with_file(self):
        self.fstree.add_path('dir', sentinel.dir_stat)
        self.fstree.add_path('dir/file', sentinel.file_stat, False)
        self.assertEqual([('dir', sentinel.dir_stat, True, [
            ('dir/file', sentinel.file_stat, False, []),
        ])], store_to_list(self.fstree.store))

    def test_add_dir_with_files(self):
        self.fstree.add_path('dir', sentinel.dir_stat)
        self.fstree.add_path('dir/foo', sentinel.foo_stat, False)
        self.fstree.add_path('dir/bar', sentinel.bar_stat, False)
        self.assertEqual([('bar', sentinel.dir_stat, True, [
            ('bar', sentinel.bar_stat, False, []),
            ('foo', sentinel.foo_stat, False, [])
        ])], store_to_list(self.fstree.store))


def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestFSTree)

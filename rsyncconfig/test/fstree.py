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


class TestFSTree(unittest.TestCase):
    def setUp(self):
        self.fstree = FSTree()

    def testSingleFile(self):
        self.fstree.add_path('foo', sentinel.file_stat, True)
        self.assertEqual([('foo', sentinel.file_stat, True)],
                         list(self.fstree.store))

def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestFSTree)

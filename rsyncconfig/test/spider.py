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
Tests for the rsyncconfig.spider module
'''

import os
import time
import unittest
from contextlib import nested

from mock import patch, sentinel, Mock

from rsyncconfig.spider import Spider


class TestSpider(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.os_mocks = nested(
            patch('os.listdir'),
            patch('os.lstat'),
        )

    def setUp(self):
        self.fstree = Mock(name='fstree',
                           spec=['add_path', 'update_path', 'remove_path'])

    def test_empty(self):
        with self.os_mocks as (listdir, lstat):
            listdir.return_value = []

            spider = Spider(self.fstree, '.')
            time.sleep(0.01)
            spider.stop()

            listdir.assert_called_with('.')
            self.assertFalse(self.fstree.add_path.called)


def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestSpider)

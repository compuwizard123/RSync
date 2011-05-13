# encoding: utf-8

# Copyright (C) 2011 Kevin J. Risden
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
Tests for the rsyncconfig.filterruleset module
'''

import os
import unittest
from stat import *

from rsyncconfig.filter import FilterRuleset

FILE_STAT = os.stat(__file__)
assert S_ISREG(FILE_STAT.st_mode)

DIR_STAT = os.stat(os.path.dirname(__file__))
assert S_ISDIR(DIR_STAT.st_mode)

class TestFilterRuleset(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_filters(self):
        '''
        '''
        frs = FilterRuleset("")

def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestFilterRuleset)

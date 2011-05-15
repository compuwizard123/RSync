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
        frs = FilterRuleset("");
        self.assertTrue(frs.apply('test', FILE_STAT));
        self.assertTrue(frs.apply('test', DIR_STAT));

    def test_comment_filter(self):
        frs = FilterRuleset(";exclude /test\ninclude test2");
        self.assertTrue(frs.apply('test/test2', FILE_STAT));
        self.assertTrue(frs.apply('test/test2', DIR_STAT));

    def test_one_include_filter(self):
        frs = FilterRuleset("include test");
        self.assertTrue(frs.apply('test', FILE_STAT));
        self.assertTrue(frs.apply('test', DIR_STAT));
        self.assertTrue(frs.apply('test2', FILE_STAT));
        self.assertTrue(frs.apply('test2', DIR_STAT));

    def test_one_plus_filter(self):
        frs = FilterRuleset("+ test");
        self.assertTrue(frs.apply('test', FILE_STAT));
        self.assertTrue(frs.apply('test', DIR_STAT));
        self.assertTrue(frs.apply('test2', FILE_STAT));
        self.assertTrue(frs.apply('test2', DIR_STAT));

    def test_one_exclude_filter(self):
        frs = FilterRuleset("exclude test");
        self.assertFalse(frs.apply('test', FILE_STAT));
        self.assertFalse(frs.apply('test', DIR_STAT));
        self.assertTrue(frs.apply('testing', FILE_STAT));
        self.assertTrue(frs.apply('testing', DIR_STAT));

    def test_one_minus_filter(self):
        frs = FilterRuleset("- test");
        self.assertFalse(frs.apply('test', FILE_STAT));
        self.assertFalse(frs.apply('test', DIR_STAT));
        self.assertTrue(frs.apply('testing', FILE_STAT));
        self.assertTrue(frs.apply('testing', DIR_STAT));

    def test_many_include_filters(self):
        frs = FilterRuleset("include test\ninclude test2");
        self.assertTrue(frs.apply('test', FILE_STAT));
        self.assertTrue(frs.apply('test', DIR_STAT));
        self.assertTrue(frs.apply('test2', FILE_STAT));
        self.assertTrue(frs.apply('test2', DIR_STAT));
        self.assertTrue(frs.apply('test3', FILE_STAT));
        self.assertTrue(frs.apply('test3', DIR_STAT));

    def test_many_plus_filters(self):
        frs = FilterRuleset("+ test\n+ test2");
        self.assertTrue(frs.apply('test', FILE_STAT));
        self.assertTrue(frs.apply('test', DIR_STAT));
        self.assertTrue(frs.apply('test2', FILE_STAT));
        self.assertTrue(frs.apply('test2', DIR_STAT));
        self.assertTrue(frs.apply('test3', FILE_STAT));
        self.assertTrue(frs.apply('test3', DIR_STAT));

    def test_many_exclude_filters(self):
        frs = FilterRuleset("exclude test\nexclude test2");
        self.assertFalse(frs.apply('test', FILE_STAT));
        self.assertFalse(frs.apply('test', DIR_STAT));
        self.assertFalse(frs.apply('test2', FILE_STAT));
        self.assertFalse(frs.apply('test2', DIR_STAT));
        self.assertTrue(frs.apply('test3', FILE_STAT));
        self.assertTrue(frs.apply('test3', DIR_STAT));

    def test_many_minus_filters(self):
        frs = FilterRuleset("- test\n- test2");
        self.assertFalse(frs.apply('test', FILE_STAT));
        self.assertFalse(frs.apply('test', DIR_STAT));
        self.assertFalse(frs.apply('test2', FILE_STAT));
        self.assertFalse(frs.apply('test2', DIR_STAT));
        self.assertTrue(frs.apply('test3', FILE_STAT));
        self.assertTrue(frs.apply('test3', DIR_STAT));

    def test_mixed_filters(self):
        frs = FilterRuleset("exclude test1\ninclude test2/*\n- test3\n+ test4");
        self.assertFalse(frs.apply('test1', FILE_STAT));
        self.assertFalse(frs.apply('test1', DIR_STAT));
        self.assertTrue(frs.apply('test2', FILE_STAT));
        self.assertTrue(frs.apply('test2', DIR_STAT));
        self.assertFalse(frs.apply('test3', FILE_STAT));
        self.assertFalse(frs.apply('test3', DIR_STAT));
        self.assertTrue(frs.apply('test4', FILE_STAT));
        self.assertTrue(frs.apply('test4', DIR_STAT));
        self.assertFalse(frs.apply('test2/test1', FILE_STAT));
        self.assertFalse(frs.apply('test2/test1', DIR_STAT));
        self.assertTrue(frs.apply('test2/test3', FILE_STAT));
        self.assertTrue(frs.apply('test2/test3', DIR_STAT));

def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestFilterRuleset)

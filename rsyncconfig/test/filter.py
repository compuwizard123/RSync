'''
Tests for the rsyncconfig.filter module
'''

import os
import unittest
from stat import *

from rsyncconfig.filter import FilterRule


class TestFileRule(unittest.TestCase):
    def setUp(self):
        # A file stat_t
        self.file_stat = os.stat(__file__)
        # A directory stat_t
        self.dir_stat = os.stat(os.path.dirname(__file__))
        # Sanity check the stats
        if not S_ISREG(self.file_stat.st_mode) or not S_ISDIR(self.dir_stat.st_mode):
            raise ValueError('Unable to get mock stats')

    def run_test_table(self, tests):
        '''
        Helper method that runs assertions for a table containing patterns,
        test values, stat values, and the expected result.  If a stat value is
        given as None then the pattern will be tested for both a file stat and
        a dir stat.
        '''
        # Heh heh heh
        def message(s):
            return "{0!r} {1} {2!r} (a {3})".format(
                pattern,
                "matches" if matches else "doesn't match",
                path,
                "directory" if S_ISDIR(s.st_mode) else "file")

        for pattern, path, stat, matches in tests:
            if stat is None:
                file_res = FilterRule(pattern).match(path, self.file_stat)
                self.assertEqual(matches, file_res, message(self.dir_stat))
                dir_res = FilterRule(pattern).match(path, self.dir_stat)
                self.assertEqual(matches, dir_res, message(self.dir_stat))
            else:
                res = FilterRule(pattern).match(path, stat)
                self.assertEqual(matches, res, message(stat))

    def test_dir_slash(self):
        '''
        Check that a trailing slash requires that the stat be a directory.
        '''
        self.run_test_table([
            ('/foo/', 'foo', self.dir_stat, True),
            ('/foo/', 'foo', self.file_stat, False),
            ('foo/', 'bar/foo', self.file_stat, False),
            ('foo/', 'bar/foo', self.dir_stat, True),
        ])


    def test_anchoring(self):
        '''
        Check that the pattern is anchored to the root if it leads with a
        slash.
        '''
        self.run_test_table([
            ('/foo', 'foo', None, True),
            ('foo', 'foo', None, True),
            ('foo', 'bar/foo', None, True),
            ('/foo', 'bar/foo', None, False),
        ])

    def test_wildcard(self):
        self.run_test_table([
            ('*', 'foo', None, True),
            ('foo.*', 'foo.bar', None, True),
            ('foo.*', 'foo.', None, True),
            ('foo.*', 'foo', None, False),
            ('foo.*', 'foo/bar', None, False),
            ('/*/foo', 'bar/foo', None, True),
            ('/*/foo', 'bar/bar', None, False),
            ('/*b/', 'ab', self.dir_stat, True),
            ('\\*', '*', None, False),
            ('\\*', '\\*', None, True),
            ('\\*', 'a', None, False),
            ('*/\\*', 'a/*', None, True),
        ])

    def test_double_wildcard(self):
        self.run_test_table([
            ('/foo/**/baz', 'foo/bar/baz', None, True),
            ('**/baz/', 'foo/bar/baz/', self.dir_stat, True),
            ('**/baz', 'foo/bar/baz', self.dir_stat, True),
            ('/**/baz', 'foo/bar/baz', None, True),
        ])

    def test_triple_wildcard(self):
        self.run_test_table([
            ('foo/***', 'foo', self.dir_stat, True),
            ('foo/***', 'foo', self.file_stat, False),
            ('foo/***', 'foo/biz', None, True),
            ('foo/***', 'a/b/foo/bar', None, False),
            ('foo/***', 'biz/foo', None, False),
            ('/*/foo/***', 'biz/foo/file', None, True),
            ('foo/***', 'biz/foo/foo spaced', None, False),
            ('/foo/***', 'foo', self.dir_stat, True),
            ('/foo/***', 'foo', self.file_stat, False),
        ])

    def test_char_class(self):
        self.assert_(False)
        pass # TODO: Test [a-z]

    def test_local_char_class(self):
        self.assert_(False)
        pass # TODO: Test [[:alpha:]]

    def test_wildchar(self):
        self.assert_(False)
        pass # TODO: Test ?
    
    def test_escaped_specials(self):
        '''
        Patterns match differently based on whether or not wildcard characters
        are present.  If they are not present (or, presumably, are all escaped,
        then they match literally (e.g., including the backslash escape).
        Otherwise escaped wildcards match as the escaped character and
        unescaped wildcards match as wildcards, as tested above.
        '''
        self.assert_(False)
        pass # TODO: Test this

suite = unittest.TestLoader().loadTestsFromTestCase(TestFileRule)

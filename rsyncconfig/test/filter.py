'''
Tests for the rsyncconfig.filter module
'''

import os
import unittest
from stat import *

from rsyncconfig.filter import FilterRule


FILE_STAT = os.stat(__file__)
if not S_ISREG(FILE_STAT.st_mode):
    raise ValueError('Unable to get mock file stat')


DIR_STAT = os.stat(os.path.dirname(__file__))
if not S_ISDIR(DIR_STAT.st_mode):
    raise ValueError('Unable to get mock dir stat')


class _FilterTestCase(unittest.TestCase):
    def __init__(self, pattern, path, stat, matches):
        unittest.TestCase.__init__(self, 'run_test')
        self._pattern = pattern
        self._path = path
        self._stat = stat
        self._matches = matches

    def run_test(self):
        fr = FilterRule(self._pattern)
        res = fr.match(self._path, self._stat)
        self.assertEqual(self._matches, res, self.get_message())

    def get_message(self):
        '''
        Generate the assertion message for the test.
        '''
        return "{0!r} {1} {2!r} (a {3})".format(
            self._pattern,
            "matches" if self._matches else "doesn't match",
            self._path,
            "directory" if S_ISDIR(self._stat.st_mode) else "file")

class _FilterTestSuite(unittest.TestSuite):
    '''
    Extends unittest.TestSuite to act as a factory for filter test cases.
    '''

    def add_test_table(self, *test_tuples):
        '''
        Add tests to this suite based on the given four-tuples of (patter,
        path, stat, matches).  If stat is None, generate a test for both
        of FILE_STAT and DIR_STAT.
        '''
        for (pattern, path, stat, matches) in test_tuples:
            if stat is None:
                for stat in (FILE_STAT, DIR_STAT):
                    self.addTest(_FilterTestCase(pattern, path, FILE_STAT, matches))
                    self.addTest(_FilterTestCase(pattern, path, DIR_STAT, matches))
            else:
                self.addTest(_FilterTestCase(pattern, path, stat, matches))


def add_tests(suite):
    # Patterns with a trailing slash must not match files.
    suite.add_test_table(
        ('/foo/', 'foo', DIR_STAT, True),
        ('/foo/', 'foo', FILE_STAT, False),
        ('foo/', 'bar/foo', FILE_STAT, False),
        ('foo/', 'bar/foo', DIR_STAT, True),
    )

    # Check that the pattern is anchored to the root if it leads with a slash.
    suite.add_test_table(
        ('/foo', 'foo', None, True),
        ('foo', 'foo', None, True),
        ('foo', 'bar/foo', None, True),
        ('/foo', 'bar/foo', None, False),
    )

    suite.add_test_table(
        ('*', 'foo', None, True),
        ('foo.*', 'foo.bar', None, True),
        ('foo.*', 'foo.', None, True),
        ('foo.*', 'foo', None, False),
        ('foo.*', 'foo/bar', None, False),
        ('/*/foo', 'bar/foo', None, True),
        ('/*/foo', 'bar/bar', None, False),
        ('/*b/', 'ab', DIR_STAT, True),
        ('\\*', '*', None, False),
        ('\\*', '\\*', None, True),
        ('\\*', 'a', None, False),
        ('*/\\*', 'a/*', None, True),
    )

    # Double wildcard can match any portion of a path.
    suite.add_test_table(
        ('/foo/**/baz', 'foo/bar/baz', None, True),
        ('**/baz/', 'foo/bar/baz/', DIR_STAT, True),
        ('**/baz', 'foo/bar/baz', DIR_STAT, True),
        ('/**/baz', 'foo/bar/baz', None, True),
    )
    
    suite.add_test_table(
        ('foo/***', 'foo', DIR_STAT, True),
        ('foo/***', 'foo', FILE_STAT, False),
        ('foo/***', 'foo/biz', None, True),
        ('foo/***', 'a/b/foo/bar', None, False),
        ('foo/***', 'biz/foo', None, False),
        ('/*/foo/***', 'biz/foo/file', None, True),
        ('foo/***', 'biz/foo/foo spaced', None, False),
        ('/foo/***', 'foo', DIR_STAT, True),
        ('/foo/***', 'foo', FILE_STAT, False),
    )

    # Test [a-z]

    suite.add_test_table(
        ('foo/*.[ch]', 'foo/bar.c', FILE_STAT, True),
        ('foo/*.[ch]', 'foo/bar.a', FILE_STAT, False),
        ('foo/*.[ch]', 'foo/bar.ch', FILE_STAT, False),
        ('foo/*.p[sy]', 'foo/bar.ps', FILE_STAT, True),
        ('foo/[a-z]/*', 'foo/q/bar', None, True),
        ('foo/[a-z]/*', 'foo/ab/bar', None, False),
    )

    # TODO: Test [[:alpha:]]

    # Test ?

    suite.add_test_table(
        ('foo/?', 'foo/bar', None, True),
        ('foo/?', 'foo/bar/', DIR_STAT, False),
        ('foo/?', 'foo/bar/a', None, False),
    )

    # Patterns match differently based on whether or not wildcard characters
    # are present.  If they are not present (or, presumably, are all escaped,
    # then they match literally (e.g., including the backslash escape).
    # Otherwise escaped wildcards match as the escaped character and unescaped
    # wildcards match as wildcards, as tested above.
    #
    # TODO

def get_suite():
    suite = _FilterTestSuite()
    add_tests(suite)
    return suite

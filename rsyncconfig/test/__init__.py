import unittest
import doctest

from . import filter
from . import spider
from . import fstree

loader = unittest.TestLoader()

def get_suite():
    return unittest.TestSuite([
        filter.get_suite(),
        spider.get_suite(),
        fstree.get_suite(),
        doctest.DocTestSuite('rsyncconfig.filter')
    ])

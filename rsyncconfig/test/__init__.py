import unittest
import doctest

from . import filter
from . import filterruleset
from . import spider
from . import fstree
from . import gui

loader = unittest.TestLoader()

def get_suite():
    return unittest.TestSuite([
        filter.get_suite(),
        filterruleset.get_suite(),
        spider.get_suite(),
        fstree.get_suite(),
        gui.get_suite(),
        doctest.DocTestSuite('rsyncconfig.filter')
    ])

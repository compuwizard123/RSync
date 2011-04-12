import unittest
import doctest

from . import filter

loader = unittest.TestLoader()

def get_suite():
    return unittest.TestSuite([
        filter.get_suite(),
        doctest.DocTestSuite('rsyncconfig.filter')
    ])

if __name__ == '__main__':
    unittest.TextTestRunner().run(get_suite())

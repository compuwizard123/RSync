import unittest
import doctest

from . import filter

loader = unittest.TestLoader()

suite = unittest.TestSuite([
    loader.loadTestsFromTestCase(filter.TestFileRule),
    doctest.DocTestSuite('rsyncconfig.filter')
])

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)

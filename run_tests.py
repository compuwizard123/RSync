#!/usr/bin/env python
'''Run the tests
'''

import unittest

from rsyncconfig.test import get_suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(get_suite())

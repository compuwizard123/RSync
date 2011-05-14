#!/usr/bin/env python
'''Run the tests

This script is assumed to be run from a development tree, so it mucks with
sys.path to make imports work.
'''

import os
import sys
# Remove the tools directory from the path
sys.path[0] = os.path.join(sys.path[0], '..')
import unittest

from rsyncconfig.test import get_suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(get_suite())

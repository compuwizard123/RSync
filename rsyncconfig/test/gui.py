# coding: utf-8

# Copyright (C) 2011 Thomas W. Most
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

'''Tests for the rbconfig.gui module
'''

import os
import shutil
import tempfile
import unittest

from .. import gui


class TestLoadGUI(unittest.TestCase):
    def test_load(self):
        '''Simple sanity check on the loading process

        Run the load_gui function and check that the most important components
        have been loaded.
        '''
        builder = gui.load_gui()
        self.assertFalse(None is builder.get_object('main_window'))
        self.assertFalse(None is builder.get_object('rootselect_filechooserbutton'))
        self.assertFalse(None is builder.get_object('fstree_treeview'))
        self.assertFalse(None is builder.get_object('main_statusbar'))
        self.assertFalse(None is builder.get_object('aboutdialog'))


class GUITestCase(unittest.TestCase):
    '''Base class for GUI test cases

    This class provides methods for constructing test directories and
    automatically constructs one defined by the test_dir_tree class variable,
    placing its location in the test_root_dir attribute.
    '''
    test_dir_tree = {} # Override in subclasses

    def setUp(self):
        '''Create the Application instance under test
        '''
        gui.init_i18n('en_US.UTF-8')
        self.test_root_dir = self.create_test_dir_tree(self.test_dir_tree)
        self.app = gui.Application()

    def tearDown(self):
        '''Delete the temporary directory
        '''
        shutil.rmtree(self.test_root_dir)

    def create_test_dir_tree(self, tree_def):
        '''Create a directory tree for test purposes

        tree_def is a dictionary, its keys defining files and directories.
        Files are represented as integers indicating the size of the file to
        generate, and directories are dictionaries as tree_def.
        '''
        dir = tempfile.mkdtemp(suffix='rsctest')
        self._populate_test_dir(dir, tree_def)
        return dir

    def _populate_test_dir(self, parent, contents):
        '''Helper that populates the given parent directory
        '''
        # We deliberately don't do any error handling here, since the tests
        # would fail erroneously if we suppressed them.
        for name, value in contents.iteritems():
            path = os.path.join(parent, name)
            if isinstance(value, int): # Number of bytes to write to a file
                with open(path, 'wb') as f:
                    while value > 0:
                        chunk_size = min(4096, value)
                        f.write('\0' * chunk_size)
                        value -= 4096
            else: # A directory
                os.mkdir(name)
                self._populate_test_dir(path, value)


class TestBasicGUIOperations(GUITestCase):
    def test_window_exists(self):
        '''Check that the main window was created when the application started
        '''
        self.assertNotEqual(self.app.window, None)


class TestSpanishTranslation(unittest.TestCase):
    def setUp(self):
        '''Create the Application instance under test
        '''
        gui.init_i18n('es_ES.UTF-8')
        self.rct = gui.Application()

    def test_window_title(self):
        self.assertEqual('Herramienta de configuracion de rsync', self.rct.window.get_title())

    # TODO: Add more tests


def get_suite():
    loader = unittest.TestLoader()
    return unittest.TestSuite([
        loader.loadTestsFromTestCase(TestLoadGUI),
        loader.loadTestsFromTestCase(TestBasicGUIOperations),
        loader.loadTestsFromTestCase(TestSpanishTranslation),
    ])

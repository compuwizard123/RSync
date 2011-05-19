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

import gtk
import mock

from .. import gui


def gtk_spin():
    '''Advance the GTK+ event loop until it runs out of events.
    '''
    while gtk.events_pending():
        gtk.main_iteration()

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


class BuilderAttrGetter(object):
    def __init__(self, builder):
        self.builder = builder

    def __getattr__(self, name):
        return self.builder.get_object(name)

class GUITestCase(unittest.TestCase):
    '''Base class for GUI test cases

    This class provides methods for constructing test directories and
    automatically constructs one defined by the test_dir_tree class variable,
    placing its location in the test_dir attribute.
    '''
    test_dir_tree = {} # Override in subclasses

    def setUp(self):
        '''Create the Application instance under test
        '''
        gui.init_i18n('en_US.UTF-8')
        self.test_dir = self.create_test_dir_tree(self.test_dir_tree)
        self.app = gui.Application()
        self.objects = BuilderAttrGetter(self.app.builder)

    def tearDown(self):
        '''Delete the test directory
        '''
        shutil.rmtree(self.test_dir)

    def create_test_dir_tree(self, tree_def):
        '''Create a directory tree for test purposes

        tree_def is a dictionary, its keys defining files and directories.
        Files are represented as integers indicating the size of the file to
        generate, and directories are dictionaries as tree_def.
        '''
        root = tempfile.mkdtemp()
        self._populate_test_dir(root, tree_def)
        return root

    def _populate_test_dir(self, parent, contents):
        '''Helper that populates the given parent directory
        '''
        # We deliberately don't do any error handling here, since the tests
        # would fail erroneously if we suppressed them.
        for name, value in contents.iteritems():
            path = os.path.join(parent, name)
            if isinstance(value, int): # Number of bytes to write to a file
                with open(path, 'wb+') as f:
                    while value > 0:
                        chunk_size = min(4096, value)
                        f.write('\0' * chunk_size)
                        value -= 4096
            elif isinstance(value, str): # String to write to a file
                with open(path, 'wb') as f:
                    f.write(value)
            else: # A directory
                os.mkdir(path)
                self._populate_test_dir(path, value)


class TestBasicGUIOperations(GUITestCase):
    def test_window_exists(self):
        '''Check that the main window was created when the application started
        '''
        self.assertNotEqual(self.app.window, None)


class TestFileMenus(GUITestCase):
    '''Test the items in the File menu

    See the docstrings for the activation handlers (in the Application class)
    for information on what they are supposed to do.
    '''
    test_dir_tree = {
        'filter_file': 'include foo\nexclude bar',
        'foo': { 'biz': 10 },
        'bar': { 'biz': 20 },
    }

    def test_file_new(self):
        self.objects.file_new_menu_item.activate()
        gtk_spin()
        self.assertEqual('', str(self.app.filters))

    def test_file_open(self):
        filter_fn = os.path.join(self.test_dir, 'filter_file')
        fcd = mock.Mock(spec=gtk.FileChooserDialog)
        fcd.get_filename.return_value = filter_fn

        with mock.patch('gtk.FileChooserDialog') as FCD:
            FCD.return_value = fcd
            self.objects.file_open_menu_item.activate()
            FCD.assert_called_with(title='Open filter file...',
                                   parent=self.app.window)

        self.assertEqual('include foo\nexclude bar',
                         str(self.app.filters), 'Read file correctly')

    @unittest.skip("Haven't mocked save dialog yet")
    def test_file_save_unsaved(self):
        self.assertTrue(self.app.filter_file is None, 'Not yet saved')
        self.objects.file_save_menu_item.activate()
        # XXX: How to mock the dialog?

    def test_file_save_again(self):
        filter_fn = os.path.join(self.test_dir, 'filter_file')

        self.app.filter_file = filter_fn
        self.objects.file_save_menu_item.activate()
        gtk_spin()

        # Check that the file was overwritten empty
        with open(filter_fn, 'rb') as f:
            self.assertEqual('', f.read(), 'File emptied')

        filter_fn2 = os.path.join(self.test_dir, 'filter_file2')
        self.app.filter_file = filter_fn2
        self.objects.file_save_menu_item.activate()
        gtk_spin()

        # Check that a new file was created, empty
        with open(filter_fn2, 'rb') as f:
            self.assertEqual('', f.read(), 'New file created empty')

    def test_file_save_as(self):
        filter_fn = os.path.join(self.test_dir, 'new_filter_fn')
        mock_dialog = mock.Mock(spec=gtk.FileChooserDialog)
        mock_dialog.get_filename.return_value = filter_fn

        with mock.patch('gtk.FileChooserDialog') as FCD:
            FCD.return_value = mock_dialog

            self.objects.file_save_as_menu_item.activate()
            gtk_spin()

            FCD.assert_called_once_with(title='Save filter file as...',
                                        parent=self.app.window)

        with open(filter_fn, 'rb') as f:
            self.assertEqual('', f.read(), 'Created file at correct location')

    def test_file_quit(self):
        '''Check that the GTK+ main loop is terminated when the application is quit
        '''
        with mock.patch('gtk.main_quit') as main_quit:
            self.objects.file_quit_menu_item.activate()
            gtk_spin()
            main_quit.assert_called_once_with()


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
        loader.loadTestsFromTestCase(TestFileMenus),
        loader.loadTestsFromTestCase(TestSpanishTranslation),
    ])

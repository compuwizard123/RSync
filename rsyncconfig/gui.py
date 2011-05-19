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

import os
import locale
import gettext
from gettext import gettext as _

import gtk

from . import GETTEXT_DOMAIN, get_pofile_dir
from .filter import FilterRuleset
from .fstree import FSTree
from .spider import Spider


def init_i18n(lang=None):
    '''Initialize internationalization libraries

    This sets the GETTEXT domain and language, if specified.  Calling this
    function is not thread-safe, as it manipulates process-wide state.  Calling
    it more than once may not be portable, as the Python locale module's
    documentation notes that this may cause some implementations to segfault.
    '''
    if lang is not None:
        os.environ['LC_ALL'] = lang
    locale.setlocale(locale.LC_ALL, '')
    locale.bindtextdomain(GETTEXT_DOMAIN, get_pofile_dir())
    gettext.bindtextdomain(GETTEXT_DOMAIN, get_pofile_dir())
    gettext.textdomain(GETTEXT_DOMAIN)
    lang2 = gettext.translation(GETTEXT_DOMAIN, get_pofile_dir())
    _ = lang2.gettext
    gettext.install(GETTEXT_DOMAIN, get_pofile_dir())


def load_gui():
    '''Load the GUI, returning a gtk.Builder instance
    '''
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    ui_file = os.path.join(data_dir, 'ui', 'mainwindow.ui')
    builder = gtk.Builder()
    builder.set_translation_domain(GETTEXT_DOMAIN)
    builder.add_from_file(ui_file)
    return builder


class Application(object):
    def __init__(self):
        self.builder = load_gui()
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('main_window')
        self.root_select_button = None
        # File the filters are saved to, or None if not yet saved
        self.filter_file = None
        self.filter_view = self.builder.get_object('filter_textview')
        self.filters = FilterRuleset('')
        self.tree = None
        self.fs_tree_view = None
        self.spider = None

    def on_main_window_destroy(self, window):
        '''When the main window is closed, terminate the mainloop
        '''
        gtk.main_quit()

    def on_file_new_menu_item_activate(self, menu_item):
        '''Create a new, empty filter file
        '''
        pass

    def on_file_open_menu_item_activate(self, menu_item):
        '''Display a dialog to open a new filter file
        '''
        chooser = gtk.FileChooserDialog(title=None,
                                        action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                        parent=self.window,
                                        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                 gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.run()
        fn = chooser.get_filename()
        if fn is not None:
            self.filter_file = fn
            self.read()

    def on_file_save_menu_item_activate(self, menu_item):
        '''Save the current filter file

        If the filter file has not yet been saved, display a dialog to save it
        under a new name.
        '''
        if self.filter_file is None:
            chooser = gtk.FileChooserDialog(title=None,
                                            action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                            parent=self.window,
                                            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                     gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            chooser.run()
            self.filter_file = chooser.get_filename()

        if self.filter_file is not None:
            self.save()

    def on_file_save_as_menu_item_activate(self, menu_item):
        '''Display a dialog to save the current filter file under a new name
        '''
        chooser = gtk.FileChooserDialog(title=None,
                                        action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        parent=self.window,
                                        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                 gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.run()
        fn = chooser.get_filename()
        if fn is not None:
            self.filter_file = fn
            self.save()

    def on_file_quit_menu_item_activate(self, menu_item):
        '''Exit the application when quit is selected in the menu
        '''
        gtk.main_quit()

    def on_help_about_menu_item_activate(self, menu_item):
        '''Display the About dialog
        '''
        pass

    def on_rootselect_filechooserbutton_file_set(self, button):
        '''Change the directory tree displayed to the one selected
        '''
        pass

    def main(self, argv):
        self.window.show()
        gtk.main()

    def read(self):
        '''Read the filter file
        '''
        with open(self.filter_file, 'rb') as f:
            text = f.read()
        self.filters = FilterRuleset(text)
        self.filter_view.get_buffer().set_text(text)

    def save(self):
        '''Save to the filter file
        '''
        with open(self.filter_file, 'wb+') as f:
            f.write(str(self.filters))

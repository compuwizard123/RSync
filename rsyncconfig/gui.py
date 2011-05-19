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

import gtk

from rsyncconfig import GETTEXT_DOMAIN, get_pofile_dir


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
    def __init__(self, base_dir):
        builder = load_gui()
        self.base_dir = base_dir
        self.window = builder.get_object('main_window')
        builder.connect_signals(self)

    def main_window_destroy_cb(self, window):
        '''When the main window is closed, terminate the mainloop
        '''
        gtk.main_quit()

    def main(self, argv):
        self.window.show()
        gtk.main()

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
import gtk

def load_gui():
    '''Load the GUI, returning a gtk.Builder instance
    '''
    data_dir = os.path.dirname(os.path.dirname(__file__))
    ui_file = os.path.join(data_dir, 'gui.ui')
    builder = gtk.Builder()
    builder.add_from_file(ui_file)
    return builder

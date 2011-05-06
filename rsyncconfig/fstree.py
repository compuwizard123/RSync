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
import stat

import gobject
import gtk

'The full file path relative to the root.'
COL_PATH = 0
'A stat of the filesystem object.'
COL_STAT = 1
'Whether the subtree of the path is currently being spidered.'
COL_SPIDERING = 2

class FSTree(object):
    '''
    Maintains a tree representation of the filesystem provided by a spider.
    '''
    def __init__(self):
        self.store = gtk.TreeStore(gobject.TYPE_STRING, 
                                   object,
                                   gobject.TYPE_BOOLEAN)
        self.store.set_sort_column_id(COL_PATH, gtk.SORT_ASCENDING)
        self._dirs = {}

    def add_path(self, path, stat_t, scanning=True):
        '''Add a path and metadata to the store.
        '''
        basedir, _ = os.path.split(path)
        if basedir:
            parent = self._dirs[basedir]
        else:
            parent = None
        iter = self.store.append(parent, (path, stat_t, scanning))
        if stat.S_ISDIR(stat_t):
            # XXX: Is keeping around iters costly?
            self._dirs[path] = iter

    def update_path(self, path, stat, scanning=False):
        '''Update a path's metadata.
        '''
        pass

    def remove_path(self, path):
        '''Remove a path from the store.
        '''
        pass

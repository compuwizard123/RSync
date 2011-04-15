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
import errno
import stat
import threading


class Spider(object):
    def __init__(self, tree, path):
        '''Create a new Spider object.

        A newly-created Spider spawns a worker thread and begins traversing the
        given path.
        '''
        self.tree = tree
        self.path = path
        self.running = True

        self.thread = threading.Thread(name=repr(self), target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def __repr__(self):
        return '{0}({1!r}, {2!r})'.format(self.__class__.__name__,
                                          self.tree, self.path)

    def run(self):
        self._process_dir(self.path)

    def _process_dir(self, dir_path):
        for path, st in self._dir_iter(dir_path):
            self.tree.add_path(path, st)
            if stat.S_ISDIR(st.st_mode):
                self._process_dir(self, path)

    def _dir_iter(self, dir_path):
        for name in os.listdir(dir_path):
            path = os.path.join(dir_path, name)
            try:
                stat = os.lstat(path)
            except EnvironmentError, e:
                if e.errno == errno.ENOENT:
                    # Race where the object has been removed from the directory
                    # since it was listed.
                    continue
                raise e
            yield path, stat

    def stop(self):
        '''Terminate the data collection process
        '''
        self.running = False

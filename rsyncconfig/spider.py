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

        self.thread = threading.Thread(target=self.run)
        self.thread.run()

    def run(self):
        for name in os.listdir(self.path):
            os.lstat(os.path.join(self.path, name))

    def stop(self):
        '''Terminate the data collection process
        '''
        self.running = False

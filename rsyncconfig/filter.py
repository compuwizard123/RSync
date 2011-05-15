# Copyright (C) 2011 Thomas W. Most
# Copyright (C) 2011 Kevin J. Risden
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

import regex
from stat import *

class FilterRuleset(object):
    #first matching pattern is acted on
    FilterRuleList = [];

    def __init__(self, filters):
        '''
        split string and store in list of FilterRules
        '''
        self.FilterRuleList = [];
        for s in filters.splitlines():
            s = s.split(' ');
            if len(s) == 2:
                if s[0] == 'include' or s[0] == '+':
                    self.FilterRuleList.append(IncludeFilter(s[1]));
                elif s[0] == 'exclude' or s[0] == '-':
                    self.FilterRuleList.append(ExcludeFilter(s[1]));

    def __str__(self):
        '''
        iterate over filter list and return newline separated string of filters
        '''
        return '\n'.join(map(str,self.FilterRuleList))

    def apply(self, path, stat):
        '''
        iterate over filter list and check match (filtered in/out)
        '''
        for rule in self.FilterRuleList:
            if rule.match(path, stat):
                if isinstance(rule, IncludeFilter):
                    return True
                elif isinstance(rule, ExcludeFilter):
                    return False
        return True

class FilterRule(object):
    def __init__(self, pattern):
        self.exp = pattern

    def match(self, path, stat):
        '''
        Return a boolean value indicating whether this rule's pattern matches
        against the given filename.  The path is the full path of the file
        relative to the transfer root, without a leading or trailing slash.
        stat is is a return value from os.stat() or os.lstat(), which indicates
        the mode of the file or directory.

        >>> import os
        >>> file_stat = os.stat(os.__file__)
        >>> FilterRule('*').match('foo/bar', file_stat)
        True
        >>> FilterRule('bar').match('foo/bar', file_stat)
        True
        >>> FilterRule('/b?oo?').match('bloof', file_stat)
        True
        >>> FilterRule('*.c').match('foo/fizzy.c', file_stat)
        True
        >>> FilterRule('/foo/**/baz').match('foo/bar/biz/baz', file_stat)
        True
        >>> FilterRule('biz/baz/').match('foo/bar/biz', file_stat)
        False
        >>> FilterRule('a[b-d]q').match('acq', file_stat)
        True
        >>> FilterRule('[[:alpha:]]').match('z', file_stat)
        True
        '''
        assert not path.endswith('/')
        assert not path.startswith('/')

        exp = self.exp

        if exp.endswith("/") and not(S_ISDIR(stat.st_mode)):
            return False
        else:
            exp = exp.rstrip("/")

        def callback(matchobj):
            mtch = matchobj.group(0)
            if mtch == '*':
                return '[^/]*'
            elif mtch == '**':
                return '.*'
            elif regex.search('\/\*\*\*', mtch):
                if S_ISDIR(stat.st_mode):
                    return '(?:/.*)?'
                else:
                    return '(?:/.*)'
            elif mtch == '?':
                return '[^/]'
            elif mtch == '/':
                return '^'
            elif mtch == '.':
                return '\.'
            else:
                return mtch

        exp = regex.sub('((^/)|(\/\*\*\*$)|(\*\*)|(\*)|(\?)|(\.))',
                        callback, exp, flags=regex.MULTILINE)
        exp = exp + '$'

        regexp = regex.compile(exp, flags=regex.DOTALL | regex.MULTILINE)
        return bool(regexp.search(path))

class ExcludeFilter(FilterRule):
    def __init__(self, pattern):
        super(ExcludeFilter, self).__init__(pattern)

    def match(self, path, stat):
        return super(ExcludeFilter, self).match(path, stat)

    def __str__(self):
        return 'exclude ' + self.exp

class IncludeFilter(FilterRule):
    def __init__(self, pattern):
        super(IncludeFilter, self).__init__(pattern)

    def match(self, path, stat):
        return super(IncludeFilter, self).match(path, stat)

    def __str__(self):
        return 'include ' + self.exp

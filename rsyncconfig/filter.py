import regex
import fnmatch
import os
from stat import *

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
        >>> FilterRule('/foo').match('foo/bar', file_stat)
        True
        >>> FilterRule('/?oo?').match('bloof', file_stat)
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
        exp = self.exp

        if exp.endswith("/") and not(S_ISDIR(stat.st_mode)):
            return False
        else:
            exp = exp.rstrip("/")

        def chkMatch(matchobj):
            mtch = matchobj.group(0)
            if mtch == '*':
                return '[^/]*'
            elif mtch == '**':
                return '.*'
            elif regex.search('\/\*\*\*',mtch) and S_ISDIR(stat.st_mode):
                return '(?:/.*)?'
            elif regex.search('\/\*\*\*',mtch) and not(S_ISDIR(stat.st_mode)):
                return '(?:.+/.+)+'
            elif mtch == '?':
                return '[^/]'
            elif mtch == '/':
                return '^'
            elif mtch == '.':
                return '\.'
            else:
                return mtch

        exp = regex.sub('((^/)|(\/\*\*\*)|(\*\*)|([a-z]*\*[a-z]*)|(\?)|(\.))',\
                            chkMatch, exp)

        regexp = regex.compile(exp)
        return True if regexp.search(path) else False

class ExcludeFilter(FilterRule):
    pass

class IncludeFilter(FilterRule):
    pass

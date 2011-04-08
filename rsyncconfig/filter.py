class FilterRule(object):
    def __init__(self, pattern):
        pass

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
        pass

class ExcludeFilter(FilterRule):
    pass

class IncludeFilter(FilterRule):
    pass

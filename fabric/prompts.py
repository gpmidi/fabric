""" React to prompts and other data interactively instead of simple run+return
"""
from __future__ import with_statement

from fabric.api import env, run
import contextlib
import re


class PromptChecker(object):
    """ Used to check IO to see if it matches according
    to the given function. 
    """

    def __init__(self, checkFunc=lambda s: False, checkFuncKW={}, useRecent=False):
        # A tad redundant in most cases; allow for non-class-based overrides
        self.checkFunc = checkFunc
        self.useRecent = useRecent
        self.checkFuncKW = checkFuncKW

    def check(self, full, recent):
        if self.useRecent:
            return self.checkFunc(recent, **self.checkFuncKW)
        else:
            return self.checkFunc(full, **self.checkFuncKW)


class ExactPromptChecker(PromptChecker):
    """ Used to check IO to see if it matches the given string
    """

    def __init__(self, matchStr, useRecent=False):
        PromptChecker.__init__(
                               self,
                               useRecent=useRecent,
                               )
        self.matchStr = matchStr


    def checkFunc(self, data):
        return self.matchStr in data


class ExactEndsWithPromptChecker(PromptChecker):
    """ Used to check IO to see if it ends with the given
    string. 
    """

    def __init__(self, matchStr, useRecent=False):
        PromptChecker.__init__(
                               self,
                               useRecent=useRecent,
                               )
        self.matchStr = matchStr


    def checkFunc(self, data):
        return data.endswith(self.matchStr)


class ExactStartsWithPromptChecker(PromptChecker):
    """ Used to check IO to see if it starts with the given
    string. 
    """

    def __init__(self, matchStr, useRecent = False):
        PromptChecker.__init__(
                               self,
                               useRecent = useRecent,
                               )
        self.matchStr = matchStr


    def checkFunc(self, data):
        return data.startswith(self.matchStr)


class RegexMatchPromptChecker(PromptChecker):
    """ Used to check IO to see if it matches the given regex 
    """
    def __init__(self, matchRE, flags = None, useRecent = False):
        """
        matchRE
        """
        PromptChecker.__init__(
                               self,
                               useRecent=useRecent,
                               )
        if hasattr(matchRE, 'match'):
            self.matchRE = matchRE
        elif isinstance(matchRE, str):
            self.matchRE = re.compile(matchRE, flags)
        else:
            raise TypeError("Object %r is not a string or a regex object" % matchRE)

    def checkFunc(self, data):
        return self.matchRE.match(data)


class RegexFindAllPromptChecker(RegexMatchPromptChecker):
    """ Used to check IO to see if it matches the given regex 
    """
    def checkFunc(self, data):
        return self.matchRE.findall(data)

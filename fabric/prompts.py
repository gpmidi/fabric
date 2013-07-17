''' React to prompts and other data
Created on Jul 17, 2013

@author: Paulson McIntyre <pmcintyre@salesforce.com>
'''
from __future__ import with_statement

from fabric.api import env, run
import contextlib
import re


class PromptChecker(object):
    """ Used to check IO to see if it matches according
    to the given function. 
    """

    def __init__(self, checkFunc=lambda s: False, checkFuncKW={}, useRecent=False):
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
                               checkFunc=self.checkFunc,
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
                               checkFunc=self.checkFunc,
                               useRecent=useRecent,
                               )
        self.matchStr = matchStr


    def checkFunc(self, data):
        return data.endswith(self.matchStr)


class RegexMatchPromptChecker(PromptChecker):
    def __init__(self, matchRE, flags=None, useRecent=False):
        PromptChecker.__init__(
                               self,
                               checkFunc=self.checkFunc,
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
    def checkFunc(self, data):
        return self.matchRE.findall(data)


class PromptContextManager(object):
    """
    """

    def __init__(self, onMatchF, prompt):
        self.prompt = prompt
        self.onMatchF = onMatchF

    def __enter__(self):
        self.save_shell = env.shell
        self.save_current_prompts = env.prompt_responses.keys()
        env.prompt_responses[self] = self.prompt

    def __exit__(self, exc_type, exc_value, traceback):
        if self not in self.save_current_prompts:
            del env.prompt_responses[self]
        else:
            pass

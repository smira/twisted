#
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

"""
The easiest way to use these functions is to do the following from your tests:
from twisted.trial.assertions import *
"""

import twisted.python.util
from twisted.python import failure
import sys

class SkipTest(Exception):
    """Raise this (with a reason) to skip the current test. You may also set
    method.skip to a reason string to skip it, or set class.skip to skip the
    entire TestCase."""

class FailTest(AssertionError):
    """Raised to indicate the current test has failed to pass."""

def fail(msg=None):
    """absolutely fails the test, do not pass go, do not collect $200

    @param msg: the message that will be displayed as the reason for the failure
    """
    raise FailTest, msg

def failIf(condition, msg=None):
    """fails the test if C{condition} evaluates to False

    @param condition: any object that defines __nonzero__
    """
    if condition:
        raise FailTest, msg
    return condition

def failUnless(condition, msg=None):
    """fails the test if C{condition} evaluates to True

    @param condition: any object that defines __nonzero__
    """
    if not condition:
        raise FailTest, msg
    return condition

def failUnlessRaises(exception, f, *args, **kwargs):
    """fails the test unless calling the function C{f} with the given C{args}
    and C{kwargs} does not raise C{exception}. The failure will report the
    traceback and call stack of the unexpected exception.

    @param exception: exception type that is to be expected
    @param f: the function to call
    """
    try:
        if not twisted.python.util.raises(exception, f, *args, **kwargs):
            raise FailTest, '%s not raised' % exception.__name__
    except FailTest, e:
        raise
    except:
        # import traceback; traceback.print_exc()
        raise FailTest, '%s raised instead of %s:\n %s' % \
              (sys.exc_info()[0], exception.__name__,
               failure.Failure().getTraceback())

def failUnlessEqual(first, second, msg=None):
    """fail the test if C{first} and C{second} are not equal
    @param msg: if msg is None, then the failure message will be '%r != %r'
                % (first, second)
    """
    if not first == second:
        raise FailTest, (msg or '%r != %r' % (first, second))
    return first

def failUnlessIdentical(first, second, msg=None):
    """fail the test if C{first} is not C{second}. This is an
    obect-identity-equality test, not an object equality (i.e. C{__eq__}) test

    @param msg: if msg is None, then the failure message will be
                '%r is not %r' % (first, second)
    """
    if first is not second:
        raise FailTest, (msg or '%r is not %r' % (first, second))
    return first

def failIfIdentical(first, second, msg=None):
    """fail the test if C{first} is C{second}. This is an
    obect-identity-equality test, not an object equality (i.e. C{__eq__}) test

    @param msg: if msg is None, then the failure message will be
                '%r is %r' % (first, second)
    """
    if first is second:
        raise FailTest, (msg or '%r is %r' % (first, second))
    return first

def failIfEqual(first, second, msg=None):
    """fail the test if C{first} == C{second}

    @param msg: if msg is None, then the failure message will be
                '%r == %r' % (first, second)
    """
    if not first != second:
        raise FailTest, (msg or '%r == %r' % (first, second))
    return first

def failUnlessIn(containee, container, msg=None):
    """fail the test if C{containee} is not found in C{container}

    @param containee: the value that should be in C{container}
    @param container: a sequence type, or in the case of a mapping type,
                      will follow semantics of 'if key in dict.keys()'
    @param msg: if msg is None, then the failure message will be
                '%r not in %r' % (first, second)
    """
    if containee not in container:
        raise FailTest, (msg or "%r not in %r" % (containee, container))
    return containee

def failIfIn(containee, container, msg=None):
    """fail the test if C{containee} is found in C{container}

    @param containee: the value that should not be in C{container}
    @param container: a sequence type, or in the case of a mapping type,
                      will follow semantics of 'if key in dict.keys()'
    @param msg: if msg is None, then the failure message will be
                '%r in %r' % (first, second)
    """
    if containee in container:
        raise FailTest, (msg or "%r in %r" % (containee, container))
    return containee


def failIfAlmostEqual(first, second, places=7, msg=None):
    """Fail if the two objects are equal as determined by their
    difference rounded to the given number of decimal places
    (default 7) and comparing to zero.

    @note: decimal places (from zero) is usually not the same
           as significant digits (measured from the most
           signficant digit).

    @note: included for compatiblity with PyUnit test cases
    """
    if round(second-first, places) == 0:
        raise FailTest, (msg or '%r == %r within %r places' %
                                             (first, second, places))

def failUnlessAlmostEqual(first, second, places=7, msg=None):
    """Fail if the two objects are unequal as determined by their
    difference rounded to the given number of decimal places
    (default 7) and comparing to zero.

    @note: decimal places (from zero) is usually not the same
           as significant digits (measured from the most
           signficant digit).

    @note: included for compatiblity with PyUnit test cases
    """
    if round(second-first, places) != 0:
        raise FailTest, (msg or '%r != %r within %r places' %
                                             (first, second, places))

def assertApproximates(first, second, tolerance, msg=None):
    """asserts that C{first} - C{second} > C{tolerance}

    @param msg: if msg is None, then the failure message will be
                '%r ~== %r' % (first, second)
    """
    if abs(first - second) > tolerance:
        raise FailTest, (msg or "%s ~== %s" % (first, second))
    return first

def assertFailure(deferred, *expectedFailures):
    """assert that deferred will errback a failure of type in expectedFailures
    """
    def _cb(ignore):
        raise FailTest, "did not catch an error, instead got %r" % (ignore,)

    return deferred.addCallbacks(_cb, lambda f: f.trap(*expectedFailures))

def failUnlessSubstring(substring, astring, msg=None):
    """a python2.2 friendly test to assert that substring is found in astring
    parameters follow the semantics of failUnlessIn
    """
    if astring.find(substring) == -1:
        raise FailTest, (msg or "%r not found in %r" % (substring, astring))

def failIfSubstring(substring, astring, msg=None):
    """a python2.2 friendly test to assert that substring is not found in
    astring parameters follow the semantics of failUnlessIn
    """
    if astring.find(substring) != -1:
        raise FailTest, (msg or "%r found in %r" % (substring, astring))

assertAlmostEqual = assertAlmostEquals = failUnlessAlmostEqual
assertNotAlmostEqual = assertNotAlmostEquals = failIfAlmostEqual
assertEqual = assertEquals = failUnlessEqual
assertNotEqual = assertNotEquals = failIfEqual
assertRaises = failUnlessRaises
assert_ = failUnless
failIfEquals = failIfEqual
assertIdentical = failUnlessIdentical
assertNotIdentical = failIfIdentical
assertIn = failUnlessIn
assertNotIn = failIfIn
failUnlessFailure = assertFailure
assertSubstring = failUnlessSubstring
assertNotSubstring = failIfSubstring


__all__ = ['fail', 'failUnlessEqual', 'failIfEqual', 'failIfEquals',
           'failUnless', 'failUnlessIdentical', 'failUnlessIn',
           'failIfIdentical', 'failIfIn', 'failIf', 'failUnlessAlmostEqual',
           'failIfAlmostEqual', 'failUnlessRaises', 'assertApproximates',
           'assertFailure', 'failUnlessSubstring', 'failIfSubstring',
           'SkipTest', 'FailTest', 'assertAlmostEqual', 'assertAlmostEquals',
           'assertNotAlmostEqual', 'assertNotAlmostEquals', 'assertEqual',
           'assertEquals', 'assertNotEqual', 'assertNotEquals',
           'assertRaises', 'assert_', 'assertIdentical', 'assertNotIdentical',
           'assertIn', 'assertNotIn', 'failUnlessFailure', 'assertSubstring',
           'assertNotSubstring']


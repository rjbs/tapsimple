#!/usr/bin/python

"""
This module implements functionality inspired from Perl's Test::More.
No subtest functionality has been implemented for now.
"""

# In Python 2.5, the "with" keyword can be used only after this import.
from __future__ import with_statement

import re
import sys

import TAP

# The next two module properties are used to mark tests as TODO tests,
# respectively tests to be skipped.
todo_reason = None
skip_reason = None

# Final result for entire test suite.
TEST_RESULT = None

# List of comparison operators
comparison_operators = ["<", ">", "==", ">=", "<=", "<>", "!=", "is", "is not",
                        "in", "not in"]

builder = TAP.Builder()

class TODO:
    """
    TODO tests are tests that the user expects to fail (e.g. testing
    functionality that has not yet been implemented). The tests will run
    normally, however their output will include the "TODO" flag.
    More importantly, failures of TODO tests will be considered ok and
    will not affect the test suite's final outcome. Successes of TODO tests
    will be reported as unexpected - to indicate that the todo_reason flag is
    no longer necessary.

    The TODO functionality is implemented using an instance of this
    context manager class, meant to be used together with the "with" keyword
    (available in Python 2.5 onwards). Example:
        with (TAP.More.TODO('some todo reason')):
            ok(1, ...)
            ok(1, ...)
            ok(1, ...)

    This ensures that if an exception occurs in the execution of the TODO block,
    all its remaining tests are "un-TODO-ed" automatically.
    """
    def __init__(self, todo):
        """
        Constructor for the TODO context manager class.
        Not required, but ensures that the TODO reason is associated with the
        TODO block:
            with TODO("todo reason"):
                ...
        """
        self.todo_reason = todo

    def __enter__(self):
        """
        The __enter__ method is required for any context manager.
        In our case, all we want it to do is to set the todo_reason module
        property to reflect the internal todo_reason.
        """
        global todo_reason

        todo_reason = self.todo_reason

    def __exit__(self, exc_type, exc_value, traceback):
        """
        The __exit__ method is required for any context manager.
        In our case, all we want it to do is to reset the internal todo_reason
        module property to None.
        Should it be called due to an exception, it will just let it propagate
        further.
        """
        global todo_reason

        todo_reason = None

class SKIP:
    """
    Skipping tests can be useful in cases in which running some of the tests is
    not useful (e.g. a product that doesn't support certain features for which
    tests were implemented anyway).

    The SKIP functionality is implemented using an instance of this
    context manager class, meant to be used together with the "with" keyword
    (available in Python 2.5 onwards). Example:
        with (TAP.More.SKIP('some skip reason')):
            ok(1, ...)
            ok(1, ...)
            ok(1, ...)

    This ensures that if an exception occurs in the execution of the SKIP block,
    all its remaining tests are "un-SKIP-ped" automatically.
    """
    def __init__(self, skip):
        """
        Constructor for the SKIP context manager class.
        Not required, but ensures that the SKIP reason is associated with the
        SKIP block:
            with SKIP("skip reason"):
                ...
        """
        self.skip_reason = skip

    def __enter__(self):
        """
        The __enter__ method is required for any context manager.
        In our case, all we want it to do is to set the todo_reason module
        property to reflect the internal todo_reason.
        """
        global skip_reason

        skip_reason = self.skip_reason

    def __exit__(self, exc_type, exc_value, traceback):
        """
        The __exit__ method is required for any context manager.
        In our case, all we want it to do is to reset the internal todo_reason
        module property to None.
        Should it be called due to an exception, it will just let it propagate
        further.
        """
        global skip_reason

        skip_reason = None

def plan(plan=None):
    """
    Description:
        Created the test plan with the given number of tests.

    Parameters:
        plan: integer representing the number of tests to be run
              or `None` if the number of tests is not apriori known.

    Return: None.
    """
    builder.set_plan(plan)

def diag(message, comment=True):
    """
    Description:
        Method used to print what went wrong with a certain test step.

    Parameters:
        message: string representing what went wrong;
        comment: whether to prefix message lines with "#" (generally True).

    Return: None.
    """
    # Build prefix in case it's needed.
    prefix = ""
    if comment:
        prefix = "# "

    # Make sure that a multi-line comment has all its lines prefixed with #
    mess = "%s%s\n" % (prefix, message.replace('\n', '\n# '))
    TAP.tap_print(mess)

def BAIL_OUT(message):
    """
    Description:
        Interrupt current test suite. Meant to be used for unrecoverable errors
        preventing further testing. Displays the message and exits with the 255
        exit code.

    Parameters:
        message: string indicating reason for bailing out.

    Return: None.
    """
    TAP.tap_print("Bail out! %s\n" % message)

    close()
    plan = builder.get_plan()
    if plan is not None:
        plan.ended = True

    sys.exit(255)

def ok(okness, description):
    """
    Description:
        Evaluates test steps and updates the current test suite result.

        This will be called by all other test result evaluation methods
        in More. This ensures that SKIP and TODO cases are treated properly.

        Current implementation is based on the assumption that TODO and SKIP
        blocks don't mix.

    Parameters:
        okness: Boolean indicating whether test step succeeded or not;
        description: string representing the message to be displayed for
                     describing the test step.

    Return:
        Boolean indicating whether test passed or not.
    """
    if todo_reason != None:
        # "todo" tests should not affect final outcome, regardless of result.
        builder.ok(okness, todo=(todo_reason + " (%s)" % description))
        step_result = True
    elif skip_reason != None:
        step_result = builder.ok(True,
                                 skip=(skip_reason + " (%s)" % description))
    else:
        step_result = builder.ok(okness, description)

    global TEST_RESULT
    if step_result == False or step_result == None:
        TEST_RESULT = 'not ok'
    return step_result

def success(description):
    """
    Description:
        Declare that this test passes without doing further checks.
        Equivalent of the Test::More pass() method - but 'pass' is reserved
        in Python.

        It calls the ok() method implemented in this module instead of directly
        calling builder.ok(). This ensures todo and skip cases are handled
        properly.

    Parameters:
        description: string representing the message to be displayed for
                     describing the test step.

    Return: Boolean True.
    """
    ok(True, description)
    return True

def fail(description):
    """
    Description:
        Declare that this test fails without doing further checks.
        Equivalent of the Test::More fail() method.

        It calls the ok() method implemented in this module instead of directly
        calling builder.ok(). This ensures todo and skip cases are handled
        properly.

    Parameters:
        description: string representing the message to be displayed for
                     describing the test step.

    Return: Boolean False.
    """
    global TEST_RESULT

    ok(False, description)
    TEST_RESULT = 'not ok'
    return False

def eq(have, want, description):
    """
    Description:
        Test equality of two operands by using Python's "==" operator.
        Works on numbers, strings and boolean values.
        Also works on all objects implementing the "__eq__" method.
        And it also works for doing object comparison: it will return True
        only if have and want are the same instance of the same class.

        However, for purposes of clarity, it might be better to use is_ok()
        when comparing whether two object instances are identical.

    Parameters:
        have: first comparison operand;
        want: second comparison operand;
        description: string representing the message to be displayed for
                     describing the test step.

    Return:
        Boolean: True if compared parameters are equal; False otherwise.
    """
    okness = (have == want)
    ok(okness, description)
    if not okness:
        diag("want: %s" % want)
        diag("have: %s" % have)
    return okness

def isnt(have, want, description):
    """
    Description:
        Test equality of two operands by using Python's "=="operator.
        Works on numbers, strings and boolean values.
        Also works on all objects implementing the "__eq__" method.
        And it also works for doing object comparison: it will return True
        only if have and want are not the same instance of the same class.

    Parameters:
        have: first comparison operand;
        want: second comparison operand;
        description: string representing the message to be displayed for
                     describing the test step.

    Return:
        Boolean: False if compared parameters are equal; True otherwise.
    """
    okness = (have != want)
    ok(okness, description)
    if not okness:
        diag("want: anything but %s" % want)
        diag("have: %s" % have)
    return okness

def can_ok(obj, method_list, description):
    """
    Description:
        Check whether object or module supports all methods/attributes specified
        in a list.

    Parameters:
        obj: object or module that should support all methods in method_list
        method_list: list of strings - contains the names of the methods
                     that should be supported by the object;
        description: string representing the message to be displayed for
                     describing the test step.

    Return:
        Boolean: True if all methods are supported; False otherwise.
    """
    okness = True
    diag_string = ""
    for method in method_list:
        if not hasattr(obj, method):
            diag_string += ("method %s not supported by object\n" % method)
            okness = False

    ok(okness, description)
    if not okness:
        # Remove trailing '\n' from diag string.
        diag_string = diag_string.strip('\n')
        diag(diag_string)
    return okness

def like(got, expected, description):
    """
    Description:
        Compares a string to a regular expression and expects it to match.

    Parameters:
        got: string to be compared with regular expression;
        expected: string - regular expression against which got will be matched;
        description: string representing the message to be displayed for
                     describing the test step.

    Return:
        Boolean: True if got matches expected, otherwise False
    """
    okness = False
    mobj = re.search(expected, got)
    if mobj != None:
        okness = True

    ok(okness, description)
    if not okness:
        diag("               '%s'" % got)
        diag("does not match '%s'" % expected)
    return okness

def unlike(got, expected, description):
    """
    Description:
        Compares a string to a regular expression and expects it not to match.

    Parameters:
        got: string to be compared with regular expression;
        expected: string - regular expression against which got will be matched;
        description: string representing the message to be displayed for
                     describing the test step.

    Return:
        Boolean: False if got matches expected, otherwise True.
    """
    okness = True
    mobj = re.search(expected, got)
    if mobj != None:
        okness = False

    ok(okness, description)
    if not okness:
        diag("                     '%s'" % got)
        diag("unexpectedly matches '%s'" % expected)
    return okness

def cmp_ok(got, operator, expected, description):
    """
    Description:
        Compares two operands (got and expected) using any Python comparison
        operator. Example:
            cmp_ok(1, "is not", 2, "1 is not 2")

    Parameters:
        got: first comparison operand;
        operator: valid Python comparison operator;
        expected: second comparison operand;
        description: string representing the message to be displayed for
                     describing the test step.

    Return:
        Boolean: Truth value of "got operator expected"
    """
    # Check that supplied operator is a valid Python operator
    if operator not in comparison_operators:
        diag("Operator %s is not supported - test '%s' not run!" %
             (operator, description))

    okness = eval("got %s expected" % operator)
    ok(okness, description)
    if not okness:
        diag("'%s %s %s' evaluated as False" % (got, operator, expected))
    return okness

def close():
    """
    Description:
        Completes the current TAP report and resets the plan.

    Parameters: None.

    Return: Integer.
            - 0 if all tests successful
            - 255 if all passed but wrong # of tests run
            - otherwise how many failed (including missing or extras)
    """
    global TEST_RESULT, builder

    return_status = 0
    plan = builder.get_plan()
    if builder._plan.expected_tests != None:
        test_diff = (plan.expected_tests - plan.counter)
    else:
        test_diff = 0

    if plan.failures == 0:
        if test_diff != 0:
            return_status = 255
    else:
        return_status = plan.failures

    if return_status != 0:
        TEST_RESULT = 'not ok'
    else:
        TEST_RESULT = 'ok'

    if plan.counter == 0:
        TAP.tap_print("#: Looks like no tests were run\n")
    TAP.tap_print("#: RESULT: %s\n" % TEST_RESULT)

    # Cleanup and print summary of tests
    plan.__del__()
    TEST_RESULT = None
    # Re-create builder object to allow re-use
    builder = TAP.Builder()


    return return_status

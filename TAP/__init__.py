import sys
import atexit

TAPOUT = sys.stdout

def tap_print(message):
    """
    Description:
        This prints to a safe duplication of stdout, which cannot be redirected
        from inside the script.
        It allows tests to redirect their debug output without also redirecting
        the TAP stream.
        This is useful for separating the test "debug" stream from the test
        TAP stream.

        TAP output can only be redirected from outside the script, e.g.:
        $ ./test.py > tap_output.txt

    Parameters:
        message: string to be printed.

    Return: None.
    """
    TAPOUT.write(message)

class Plan(object):
    """ The test case manager class."""
    def __init__(self, plan):
        self.counter = 0
        self.failures = 0
        self.expected_tests = None
        self.ended = False

        if isinstance(plan, int):
            self.expected_tests = plan
            tap_print("1..%u\n" % self.expected_tests)
        elif plan == "no_plan" or plan == None:
            pass
        elif plan == "skip_all":
            tap_print("1..0 # skip all\n")
            raise SystemExit(0)
        else:
            raise TestBadPlan(plan)

    def increment_counter(self):
        self.counter += 1

    def increment_failures(self):
        self.failures += 1

    def set_expected(self, expected_tests):
        self.expected_tests = expected_tests

    def __del__(self):
        if self.ended:
            return
        if self.expected_tests is None:
            tap_print("1..%u\n" % self.counter)
        elif self.counter != self.expected_tests:
            tap_print(("# Looks like you planned %u tests but ran %u.\n"
                       % (self.expected_tests, self.counter)))

        if self.failures > 0:
            tap_print("# Failed %s out of %s\n" % (self.failures, self.counter))
        else:
            tap_print ("# All passed\n")

        self.ended = True


class Builder(object):
    def __init__(self, plan=None):
        self._plan = None
        self.current = 1
        if plan != None:
            self.set_plan(plan)

    def set_plan(self, plan):
        existing_plan = self.get_plan()
        if existing_plan != None:
            if existing_plan.expected_tests == None:
                existing_plan.set_expected(plan)
                return
            else:
                raise TestPlannedAlready(plan)
        self._plan = Plan(plan)
        atexit.register(self._plan.__del__)

    def get_plan(self):
        return self._plan

    def ok(self, is_ok, desc=None, skip=None, todo=None):
        plan = self.get_plan()
        plan.increment_counter()

        if skip and todo:
            raise TestBadDirective(self)

        if is_ok:
            report = "ok"
        else:
            if todo == None:
                self._plan.increment_failures()
            report = "not ok"

        tap_print("%s %u" % (report, plan.counter))

        if desc:
            tap_print(" - %s" % desc)
        if skip:
            tap_print(" # SKIP %s" % skip)
        if todo:
            unexpected = ""
            if is_ok:
                unexpected = " - UNEXPECTED SUCCESS -"
            tap_print(" # TODO%s %s" % (unexpected, todo))

        tap_print("\n")

        return is_ok

class TestPlannedAlready(Exception):
    def __init__(self, plan):
        self.plan    = plan

    def __str__(self):
        return "tried to plan twice; second plan: %s" % self.plan

class TestWithoutPlan(Exception):
    def __str__(self):
        return "tried running tests without a plan"

class TestBadPlan(Exception):
    def __init__(self, plan):
        self.plan = plan

    def __str__(self):
        return "didn't understand plan '%s'" % self.plan

class TestBadDirective(Exception):
    def __str__(self):
        return "tried running a test with more than one directive"

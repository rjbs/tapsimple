#!/usr/bin/env python
# TEST SOME STUFF
from TAP.Simple import *

plan(3)

def in_between(value, bottom, top, msg):
    ret = ok(((bottom <= value) and (value <= top)), msg)
    if (not ret):
        diag("value %s is not between %s and %s" % (value, bottom, top))
    return ret

in_between(5, 3, 10, "5 is OK.")

in_between(5.5, 5, 6, "5[2] is OK.")

# This will fail.
in_between(1, 20, 30, "1 is in range.")

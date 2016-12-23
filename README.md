This is a module for Python that emits TAP (= the Test Anything Protocol).

See:

- http://testanything.org/
- https://en.wikipedia.org/wiki/Test_Anything_Protocol

## SYNOPSIS

Put this in `ok3.t` (also available under the [examples/](examples/)
directory.

```python
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
```

Now you can run:

```
$ prove examples/ok3.t
examples/ok3.t .. Failed 1/3 subtests

Test Summary Report
-------------------
examples/ok3.t (Wstat: 0 Tests: 3 Failed: 1)
  Failed test:  3
Files=1, Tests=3,  1 wallclock secs ( 0.05 usr  0.01 sys +  0.02 cusr  0.00 csys =  0.08 CPU)
Result: FAIL
```

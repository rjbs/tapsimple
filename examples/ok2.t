#!/usr/bin/env python
# TEST SOME STUFF
from TAP.Simple import *

plan(15)

ok(1)
ok(1, "everything is OK!")
ok(0, "always fails")

is_ok(10, 10, "is ten ten?")
is_ok(ok, ok, "even ok is ok!")
ok(id(ok),    "ok is not the null pointer")
ok(True,      "the Truth will set you ok")
ok(not False, "and nothing but the truth")
ok(False,     "and we'll know if you lie to us")

isa_ok(10, int, "10")
isa_ok('ok', str, "some string")

ok(0,    "zero is true", todo="be more like Ruby!")
ok(None, "none is true", skip="not possible in this universe")

eq_ok("not", "equal", "two strings are not equal");

#!/usr/bin/env python
# TEST SOME STUFF
import TAP

# plan 15 tests, only make 13
ok = TAP.Builder.create(15).ok

ok(1)
ok(1, "everything is OK!")
ok(0, "always fails")

ok(10 == 10,  "is ten ten?")
ok(ok is ok,  "even ok is ok!")
ok(id(ok),    "ok is not the null pointer")
ok(True,      "the Truth will set you ok")
ok(not False, "and nothing but the truth")
ok(False,     "and we'll know if you lie to us")

ok(isinstance(10,int),   "10 is an integer")
ok(isinstance("ok",str), "and this is an extra test")

ok(0,    "zero is true", todo="be more like Ruby!")
ok(None, "none is true", skip="not possible in this universe")

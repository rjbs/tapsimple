
import TAP
import re

builder = TAP.Builder()

def plan(plan, plan_param=None):
  builder.set_plan(plan, plan_param)

ok = builder.ok

def diag(comment):
  print "# %s" % re.compile("\n(.)").sub(comment, '\n#\1')

def eq_ok(got, expected, comment):
  okness = got == expected
  ok(okness, comment)
  if not okness:
    diag("expected: %s" % expected)
    diag("     got: %s" % got)
  return okness

def is_ok(got, expected, comment):
  okness = got is expected
  ok(okness, comment)
  if not okness:
    diag("expected id: %s" % id(expected))
    diag("     got id: %s" % id(got))
  return okness

def isa_ok(object, cls, object_name="the object"):
  okness = isinstance(object, cls)
  ok(okness, object_name + " is a " + repr(cls))
  # if not okness:
  #   diag("expected id: %s" % id(expected))
  #   diag("     got id: %s" % id(got))
  return okness

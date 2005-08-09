
import TAP

builder = TAP.Builder()

def plan(plan, plan_param=None):
  builder.set_plan(plan, plan_param)

ok = builder.ok

def diag(comment):
  print "# %s" % comment

def eq_ok(got, expected, comment):
  okness = got == expected
  ok(okness, comment)
  if not okness:
    diag("expected: %s" % expected)
    diag("     got: %s" % got)


def is_ok(got, expected, comment):
  okness = got is expected
  ok(okness, comment)
  if not okness:
    diag("expected id: %s" % id(expected))
    diag("     got id: %s" % id(got))

def isa_ok(object, cls, object_name="the object"):
  okness = isinstance(object, cls)
  ok(okness, comment)
  if not okness:
    diag("expected id: %s" % id(expected))
    diag("     got id: %s" % id(got))

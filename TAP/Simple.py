
import TAP
import sys
import re

builder = TAP.Builder()

def plan(plan=None):
    builder.set_plan(plan)

def diag(comment, hash=True):
    prefix = ""
    if hash:
        prefix  = "# "

    # Make sure that a multi-line comment has all its lines prefixed with #
    mess = "%s%s\n" % (prefix, comment.replace('\n', '\n# '))
    TAP.tap_print(mess)

def eq_ok(have, want, comment):
    okness = have == want
    builder.ok(okness, comment)
    if not okness:
        diag("want: %s" % want)
        diag("have: %s" % have)
    return okness

def ok(okness, desc=None, skip=None, todo=None):
    builder.ok(okness, desc, skip, todo)
    return okness

def is_ok(have, want, comment):
    okness = have is want
    builder.ok(okness, comment)
    if not okness:
        diag("want id: %s" % id(want))
        diag("have id: %s" % id(have))
    return okness

def isa_ok(object, cls, object_name="the object"):
    comment = object_name + " is a " + repr(cls)

    okness = isinstance(object, cls)
    builder.ok(okness, comment)
    if not okness:
        diag("want: %s is a %s" % (object_name, repr(cls)))
        diag("have : %s is a %s" % (object_name, type(object)))
    return okness


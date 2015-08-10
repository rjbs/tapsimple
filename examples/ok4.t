#!/usr/bin/env python
# TEST SOME STUFF
from TAP.Simple import *

plan(4)

import_ok("import sys", "Sys module import")
import_ok("from sys import *", "Sys module import with splat")
import_ok("import garglesplat", "Garglesplat module should not exist")
import_ok("from sys import garglesplat", "Garglesplat isn't in sys either.")

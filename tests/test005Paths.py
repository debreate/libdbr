
# ****************************************************
# * Copyright (C) 2023 - Jordan Irwin (AntumDeluge)  *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: docs/LICENSE.txt for details.               *
# ****************************************************

import os
import sys

from libdbr          import paths
from libdbr.unittest import assertEquals


def init():
  a = "foo"; b = "bar"; c = "baz"
  subject = a + os.sep + b + os.sep + c

  assertEquals(subject, paths.join(a, b, c))
  assertEquals(subject, paths.join((a, b, c)))
  assertEquals(subject, paths.join([a, b, c]))
  assertEquals(subject, paths.join(subject))
  assertEquals(subject, paths.join(a, (b, c)))
  assertEquals(subject, paths.join((a, b), c))
  assertEquals(subject, paths.join(a, [b, c]))
  assertEquals(subject, paths.join([a, b], c))
  assertEquals("foobarbaz", paths.join(a + b + c))
  assertEquals("foobar" + os.sep + "baz", paths.join(a + b, c))
  assertEquals(".", paths.join())

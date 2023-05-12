
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

import os
import sys

from libdbr          import fileio
from libdbr          import paths
from libdbr.bin      import trash
from libdbr.logger   import Logger
from libdbr.unittest import assertEquals
from libdbr.unittest import assertFalse
from libdbr.unittest import assertTrue


__logger = Logger(__name__)

def init():
  if sys.platform != "win32":
    __logger.warn("FIXME: trashing files fails on Ubuntu workflow runner")
    return 0

  root_sandbox = paths.join(paths.getAppDir(), "tests/sandbox")
  if not os.path.isdir(root_sandbox):
    fileio.makeDir(root_sandbox)
  file_trash = paths.join(root_sandbox, "trashme.txt")
  assertFalse(os.path.lexists(file_trash))
  fileio.touch(file_trash)
  assertTrue(os.path.isfile(file_trash))
  err = trash(file_trash)
  assertEquals(0, err)
  assertFalse(os.path.lexists(file_trash))


# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

import os

from libdbr          import fileio
from libdbr          import paths
from libdbr.bin      import trash
from libdbr.unittest import assertFalse
from libdbr.unittest import assertTrue


def init():
  root_sandbox = paths.join(paths.getAppDir(), "tests/sandbox")
  if not os.path.isdir(root_sandbox):
    fileio.makeDir(root_sandbox)
  file_trash = paths.join(root_sandbox, "trashme.txt")
  assertFalse(os.path.lexists(file_trash))
  fileio.touch(file_trash)
  assertTrue(os.path.isfile(file_trash))
  trash(file_trash)
  assertFalse(os.path.lexists(file_trash))

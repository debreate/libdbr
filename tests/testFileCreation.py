
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

import os

from libdbr          import fileio
from libdbr          import paths
from libdbr.unittest import assertFalse
from libdbr.unittest import assertTrue


def init():
  dir_sandbox = paths.join(paths.getAppDir(), "tests/sandbox")
  assertTrue(os.path.isdir(dir_sandbox))

  file_test = paths.join(dir_sandbox, "test_create_file.txt")
  assertFalse(os.path.exists(file_test))
  fileio.createFile(file_test)
  assertTrue(os.path.isfile(file_test))
  fileio.deleteFile(file_test)
  assertFalse(os.path.exists(file_test))

  file_test = paths.join(dir_sandbox, "test_create_file.bin")
  assertFalse(os.path.exists(file_test))
  fileio.createFile(file_test, binary=True)
  assertTrue(os.path.isfile(file_test))
  fileio.deleteFile(file_test)
  assertFalse(os.path.exists(file_test))

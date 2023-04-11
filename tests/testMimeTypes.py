
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

import os

from libdbr          import fileinfo
from libdbr          import fileio
from libdbr          import paths
from libdbr.unittest import assertEquals
from libdbr.unittest import assertFalse
from libdbr.unittest import assertNone
from libdbr.unittest import assertTrue


def init():
  # TODO: more tests

  cmd_file_exists = paths.commandExists("file")
  dir_sandbox = paths.join(paths.getAppDir(), "tests/sandbox")

  file_dummy = paths.join(dir_sandbox, "dummy1.txt")
  assertTrue(os.path.isfile(file_dummy))
  assertEquals("text/plain", fileinfo.getMimeType(file_dummy))

  file_dummy = paths.join(dir_sandbox, "dummy_one.txt")
  assertFalse(os.path.exists(file_dummy))
  assertEquals("text/plain", fileinfo.getMimeType(file_dummy))

  file_dummy = paths.join(dir_sandbox, "dummy1")
  assertFalse(os.path.exists(file_dummy))
  assertNone(fileinfo.getMimeType(file_dummy))
  fileio.touch(file_dummy)
  assertTrue(os.path.isfile(file_dummy))
  if cmd_file_exists:
    assertEquals("inode/x-empty", fileinfo.getMimeType(file_dummy))
    fileio.writeFile(file_dummy, "foobar")
    assertEquals("text/plain", fileinfo.getMimeType(file_dummy))
  else:
    assertEquals(fileinfo.__default, fileinfo.getMimeType(file_dummy))
  fileio.deleteFile(file_dummy)
  assertFalse(os.path.isfile(file_dummy))

  file_dummy = paths.join(dir_sandbox, "dummy1.py")
  assertFalse(os.path.exists(file_dummy))
  assertEquals("application/x-python", fileinfo.getMimeType(file_dummy))
  if cmd_file_exists:
    fileio.touch(file_dummy)
    assertTrue(os.path.isfile(file_dummy))
    assertEquals("inode/x-empty", fileinfo.getMimeType(file_dummy))
    fileio.writeFile(file_dummy, "#!/usr/bin/env python\n")
    assertEquals("text/x-script.python", fileinfo.getMimeType(file_dummy))
    fileio.deleteFile(file_dummy)
    assertFalse(os.path.exists(file_dummy))

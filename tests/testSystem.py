
# ****************************************************
# * Copyright (C) 2023 - Jordan Irwin (AntumDeluge)  *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: docs/LICENSE.txt for details.               *
# ****************************************************

import os
import sys

from libdbr          import fileinfo
from libdbr          import paths
from libdbr          import sysinfo
from libdbr.logger   import Logger
from libdbr.unittest import assertEquals
from libdbr.unittest import assertFalse
from libdbr.unittest import assertNotEquals
from libdbr.unittest import assertTrue


__logger = Logger(__name__)
__os_name = sysinfo.getOSName()

def init():
  checkOSName()
  checkPathSeparator()
  checkSystemRoot()
  checkExecutables()

def checkOSName():
  os_name = sysinfo.getOSName()
  __logger.debug("OS name: {}".format(os_name))
  if sys.platform != "win32":
    assertNotEquals("win32", os_name)
  elif os_name != sys.platform:
    assertEquals("msys", os_name)

def checkPathSeparator():
  msys = os.getenv("MSYSTEM")
  if msys and msys.lower() in sysinfo.__msys:
    assertEquals("msys", __os_name)
  elif sys.platform == "win32":
    assertEquals("win32", __os_name)

  if sys.platform == "win32":
    if __os_name == "msys":
      assertEquals("/", os.sep)
    else:
      assertEquals("\\", os.sep)
  else:
    assertEquals("/", os.sep)

def checkSystemRoot():
  sys_root = paths.getSystemRoot()
  if __os_name == "win32":
    assertEquals(os.getenv("SystemDrive") + "\\", sys_root)
  else:
    assertEquals("/", paths.getSubSystemRoot())

def checkExecutables():
  # check for common system dependent executable files
  shell = paths.normalize("/usr/bin/sh")
  if sys.platform == "win32":
    if __os_name == "win32":
      shell = paths.join(paths.getSystemRoot(), "Windows", "System32", "cmd.exe")
    else:
      print("SUBSYTEM")
      shell = paths.normalize("/usr/bin/shell")
  elif not os.path.exists(shell) or os.path.isdir(shell):
    shell = paths.normalize("/bin/sh")
  __logger.debug("checking for shell '{}'".format(shell))
  assertTrue(os.path.exists(shell))
  assertFalse(os.path.isdir(shell))
  assertTrue(fileinfo.isExecutable(shell))

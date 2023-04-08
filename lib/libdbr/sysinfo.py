
# ****************************************************
# * Copyright (C) 2023 - Jordan Irwin (AntumDeluge)  *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

import os
import sys

from libdbr import config


# MSYS/MinGW platforms
__msys_list = ("msys", "mingw32", "mingw64", "clang32", "clang64", "clangarm64", "ucrt64")

__core_name = sys.platform
if __core_name == "win32":
  __os_name = __core_name
  __msys = (os.getenv("MSYSTEM") or "").lower()
  if __msys in __msys_list:
    __os_name = "msys"
    __core_name = __msys
else:
  if os.path.isfile("/etc/lsb-release"):
    __os_name = config.getValue("DISTRIB_ID", filepath="/etc/lsb-release")
if not __os_name:
  __os_name = "unknown"
__os_name = __os_name.lower()

## Retrieves detected operating system name.
def getOSName():
  return __os_name

## Retrieves the system core name.
def getCoreName():
  return __core_name
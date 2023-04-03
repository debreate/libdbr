
# ****************************************************
# * Copyright (C) 2023 - Jordan Irwin (AntumDeluge)  *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

# Python module handling

import errno
import subprocess
import sys

from libdbr.logger import getLogger


logger = getLogger()
installed = {}

## Installs a Python module.
#
#  If module is not installed on system, attempts to download & install using pip. Module is then
#  cached.
#
#  @param name
#    Canonical name of module to be imported.
#  @param package
#    Optional package name which contains module.
#  @return
#    0 for success.
def installModule(name, package=None):
  if package == None:
    package = name
  if name in installed:
    logger.warn("not re-installing module: {}".format(name))
    return 0
  try:
    installed[name] = __import__(name)
    logger.warn("not re-installing module: {}".format(name))
    return 0
  except ModuleNotFoundError:
    pass
  logger.info("installing module: {}".format(name))
  subprocess.run((sys.executable, "-m", "pip", "install", package))
  res = 0
  try:
    installed[name] = __import__(name)
  except ModuleNotFoundError:
    logger.error("unable to install module: {}".format(name))
    res = errno.ENOENT
  return res

## Attempts to retrieve an installed module.
#
#  @param name
#    Canonical name of module.
#  @return
#    Imported module object or `None`.
def getModule(name):
  if name not in installed:
    try:
      installed[name] = __import__(name)
    except ModuleNotFoundError:
      logger.warn("module not available: {}".format(name))
      return None
  return installed[name]

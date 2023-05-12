
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

import os
import sys

from libdbr          import paths
from libdbr          import sysinfo
from libdbr.logger   import Logger
from libdbr.unittest import assertNone
from libdbr.unittest import assertNotNone
from libdbr.unittest import assertTrue


__logger = Logger(__name__)

def init():
  bit_length = sysinfo.getBitLength()

  cmd_file = paths.getExecutable("file")
  cmd_recycle = paths.getExecutable("recycle-bin")
  cmd_gio = paths.getExecutable("gio")

  __logger.debug("file command: {}".format(cmd_file))
  __logger.debug("recycle-bin command: {}".format(cmd_recycle))
  __logger.debug("gio command: {}".format(cmd_gio))

  assertNotNone(cmd_file)
  if sys.platform == "win32":
    assertNotNone(cmd_recycle)
    assertNone(cmd_gio)

    assertTrue(os.path.dirname(cmd_file)
        .endswith("utilities" + os.sep + "win{}".format(bit_length)))
    assertTrue(os.path.dirname(cmd_recycle)
        .endswith("utilities" + os.sep + "win{}".format(bit_length)))
  else:
    assertNone(cmd_recycle)
    assertNotNone(cmd_gio)

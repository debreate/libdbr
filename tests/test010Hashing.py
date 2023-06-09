
# ****************************************************
# * Copyright (C) 2023 - Jordan Irwin (AntumDeluge)  *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: docs/LICENSE.txt for details.               *
# ****************************************************

from libdbr          import fileio
from libdbr          import paths
from libdbr.misc     import generateMD5Hash
from libdbr.unittest import assertEquals


def init():
  test_file = paths.join(paths.getAppDir(), "tests/sandbox/generate_hash_test")
  # generated with `md5sum` command
  md5sum_hash = "ca8e6c1a31653fe6b917013868a49915"
  libdbr_hash = generateMD5Hash(fileio.readFile(test_file))
  assertEquals(md5sum_hash, libdbr_hash)

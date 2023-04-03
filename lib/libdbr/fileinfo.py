
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

from libdbr     import paths
from libdbr.bin import execute


__default = "application/octet-stream"

## Retrieve MimeType info for file.
#
#  @param filepath
#    Path to file.
#  @return
#    MimeType ID string.
def getMimeType(filepath):
  # FIXME: need platform independent method to get mimetypes
  cmd_file = paths.getExecutable("file")
  if not cmd_file:
    return __default
  code, output = execute(cmd_file, "--mime-type", "--brief", filepath)
  # 'file' command always returns 0
  if not output or "cannot open" in output:
    return __default
  return output

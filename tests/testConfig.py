
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

import os

from libdbr          import config
from libdbr          import fileio
from libdbr          import paths
from libdbr.unittest import assertEquals
from libdbr.unittest import assertFalse
from libdbr.unittest import assertNone
from libdbr.unittest import assertNotEquals
from libdbr.unittest import assertTrue


def init():
  dir_sandbox = paths.join(paths.getAppDir(), "tests/sandbox")
  filepathA = paths.join(dir_sandbox, "test_config_a.conf")
  filepathB = paths.join(dir_sandbox, "test_config_b.conf")
  assertFalse(os.path.exists(filepathA))
  assertFalse(os.path.exists(filepathB))

  # ~ cfgA = config.Config(filepathA)
  cfgA = config.add("A", filepathA)
  assertTrue(config.get("A") is cfgA)
  assertEquals(filepathA, cfgA.getFile())

  # try to load non-existing file
  assertNotEquals(0, cfgA.load()[0])

  createFile(filepathA)
  assertTrue(os.path.isfile(filepathA))

  assertEquals(0, cfgA.load()[0])

  # ~ cfgB = config.Config(filepathB)
  cfgB = config.add("B", filepathB)
  assertEquals(filepathB, cfgB.getFile())
  cfgB.setFile(filepathA)
  assertEquals(filepathA, cfgB.getFile())
  assertEquals(0, cfgB.load()[0])
  cfgB.setFile(filepathB)
  cfgB.save()
  assertTrue(os.path.isfile(filepathB))

  contentA = fileio.readFile(filepathA)
  contentB = fileio.readFile(filepathB)
  assertNotEquals(contentA, contentB)

  cfgA.setFile(filepathB)
  assertEquals(0, cfgA.load()[0])
  cfgA.setFile(filepathA)

  # DEBUG:
  # ~ print("sectionsA: {}".format(list(cfgA._Config__sections)))
  # ~ print("sectionsB: {}".format(list(cfgB._Config__sections)))

  assertEquals(tuple(cfgA._Config__sections), tuple(cfgB._Config__sections))
  assertEquals(cfgB, cfgA)

  assertEquals(("str1", "str2", "str3", "str4", "str5", "str6", "str7"), cfgA.getKeys())
  assertEquals(("kvpair1", "kvpair2", "kvpair3", "kvpair4"), cfgA.getKeys(section="kvpairs"))

  assertEquals("value6", cfgA.getValue("str6"))
  assertEquals("foo", cfgA.getValue("str8", default="foo"))
  assertEquals("bar", cfgA.getValue("str1", default="bar", section="numbers"))
  assertEquals("5.5", cfgA.getValue("float", section="numbers"))
  assertEquals("baz", cfgA.getValue("float", default="baz", section=""))
  assertEquals("a=b;c=d", cfgA.getValue("kvpair3", default="foo", section="kvpairs"))

  assertEquals(5, cfgA.getFloat("int", section="numbers"))
  assertEquals(5.5, cfgA.getFloat("float", section="numbers"))
  assertEquals(5, cfgA.getInt("int", section="numbers"))
  assertEquals(5, cfgA.getInt("float", section="numbers"))

  for x in ("true", "false", "yes", "no", "nzero", "zero"):
    for idx in range(1, 5):
      v = cfgA.getBool("{}{}".format(x, idx), section="bools")
      if x in ("true", "yes", "nzero"):
        assertTrue(v)
      else:
        assertFalse(v)

  dataA = fileio.readFile(filepathA)
  dataB = fileio.readFile(filepathB)
  assertNotEquals(dataB, dataA)

  cfgA.save()
  dataA = fileio.readFile(filepathA)
  assertEquals(dataB, dataA)

  fileio.deleteFile(filepathA)
  fileio.deleteFile(filepathB)
  assertFalse(os.path.exists(filepathA))
  assertFalse(os.path.exists(filepathB))

  cfgC = config.pop("A")
  assertTrue(cfgC is cfgA)
  assertNone(config.get("A"))
  assertNone(config.pop("A"))

def createFile(filepath):
  conf_data = [
    # default section
    "str1 = value1",
    "str2=value2",
    "str3 =value3",
    "# comment foo",
    "str4= value4",
    "str5\t=\tvalue5",
    "malformed line",
    "str6\t=value6",
    "str7=\tvalue7",
    "[numbers]",
    "int = 5",
    "float = 5.5",
    "[lists]",
    "list1 = a,b,c,d",
    "", # empty line
    "list2 = a;b,c;d",
    "[kvpairs]",
    "kvpair1 = a=b,c=d",
    " # comment bar",
    "kvpair2 = a:b,c:d",
    "kvpair3 = a=b;c=d",
    "kvpair4 = a:b;c:d",
    "[bools]",
    "true1 = True",
    "true2 = true",
    "true3 = truE",
    "true4 = TRUE",
    "false1 = False",
    "false2 = false",
    "false3 = falSe",
    "false4 = FALSE",
    "yes1 = Yes",
    "yes2 = yes",
    "yes3 = yeS",
    "yes4 = YES",
    "no1 = No",
    "no2 = no",
    "no3 = nO",
    "no4 = NO",
    "nzero1 = 1",
    "nzero2 = -1",
    "nzero3 = 0.1",
    "nzero4 = -0.1",
    "zero1 = 0",
    "zero2 = -0",
    "zero3 = 0.0",
    "zero4 = -0.0"
  ]
  fileio.writeFile(filepath, "\n".join(conf_data))

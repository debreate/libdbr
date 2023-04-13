
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

from libdbr.logger   import LogLevel
from libdbr.logger   import Logger
from libdbr.unittest import assertEquals
from libdbr.unittest import assertError
from libdbr.unittest import assertFalse
from libdbr.unittest import assertTrue


def init():
  levels = LogLevel.getLevels()
  levels_names = LogLevel.getLevelsNames()

  for s_level in levels_names:
    i_level = LogLevel.fromString(s_level.upper())
    assertEquals(s_level, LogLevel.toString(i_level))
    i_level = LogLevel.fromString(s_level.lower())
    assertEquals(s_level, LogLevel.toString(i_level))

  for i_level in levels:
    s_level = LogLevel.toString(i_level)
    assertEquals(i_level, LogLevel.fromString(s_level.upper()))
    assertEquals(i_level, LogLevel.fromString(s_level.lower()))

  ll_default = LogLevel.getDefault()
  assertEquals(LogLevel.INFO, LogLevel.getDefault())

  for i_level in levels:
    s_level = LogLevel.toString(i_level)
    LogLevel.setDefault(s_level)
    assertEquals(i_level, LogLevel.getDefault())

  # reset
  LogLevel.setDefault(ll_default)
  assertEquals(ll_default, LogLevel.getDefault())

  for s_level in levels_names:
    i_level = LogLevel.fromString(s_level)
    LogLevel.setDefault(i_level)
    assertEquals(i_level, LogLevel.getDefault())

  # reset
  LogLevel.setDefault(ll_default)
  assertEquals(ll_default, LogLevel.getDefault())

  assertError(LogLevel.fromString, 5)
  assertError(LogLevel.fromString, "5")
  assertError(LogLevel.fromString, "five")
  assertError(LogLevel.toString, 5)
  assertError(LogLevel.toString, "5")
  assertError(LogLevel.toString, "five")

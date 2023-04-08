
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

from libdbr.unittest import assertEquals
from libdbr.unittest import assertFalse
from libdbr.unittest import assertNone
from libdbr.unittest import assertNotEquals
from libdbr.unittest import assertNotNone
from libdbr.unittest import assertTrue


def init():
  assertTrue(True)
  assertFalse(False)
  assertTrue(True != False)
  assertFalse(True == False)
  assertEquals(True, True)
  assertEquals(False, False)
  assertNotEquals(True, False)
  assertEquals("foo", "foo")
  assertNotEquals("foo", "bar")
  assertEquals(5, 5)
  assertEquals(5.0, 5)
  assertNotEquals(5.1, 5)
  assertEquals(5.1, 5.1)
  assertEquals(["foo", "bar"], ["foo", "bar"])
  assertNotEquals(["foo", "bar"], ["foo", "bar", "baz"])
  assertNotEquals(["foo", "bar"], ["bar", "foo"])
  assertNotEquals(["foo", "bar"], 5)
  assertEquals(("foo", "bar"), ("foo", "bar"))
  assertNotEquals(("foo", "bar"), ("foo", "bar", "baz"))
  assertNotEquals(("foo", "bar"), ("bar", "foo"))
  assertNotEquals(("foo", "bar"), "foo, bar")

  try:
    assertTrue(False)
    raise Exception("failure test failed: assertTrue(False)")
  except AssertionError:
    pass
  try:
    assertFalse(True)
    raise Exception("failure test failed: assertFalse(True)")
  except AssertionError:
    pass
  try:
    assertEquals(5, 100)
    raise Exception("failure test failed: assertEquals(5, 100)")
  except AssertionError:
    pass
  try:
    assertEquals(5, "foo")
    raise Exception("failure test failed: assertEquals(5, \"foo\")")
  except AssertionError:
    pass
  try:
    assertNotEquals(5, 5)
    raise Exception("failure test failed: assertNotEquals(5, 5)")
  except AssertionError:
    pass
  try:
    assertNone("")
    raise Exception("failure test failed: assertNone(\"\")")
  except AssertionError:
    pass
  try:
    assertNotNone(None)
    raise Exception("failure test failed: assertNotNone(None)")
  except AssertionError:
    pass

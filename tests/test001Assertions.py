
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

from libdbr.unittest import assertEquals
from libdbr.unittest import assertError
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

  assertError(assertTrue, False)
  assertError(assertFalse, True)
  assertError(assertEquals, 5, 100)
  assertError(assertEquals, 5, "foo")
  assertError(assertNotEquals, 5, 5)
  assertError(assertNone, "")
  assertError(assertNotNone, None)

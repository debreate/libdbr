
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

from libdbr          import strings
from libdbr.unittest import assertTrue
from libdbr.unittest import assertEquals
from libdbr.unittest import assertFalse
from libdbr.unittest import assertNone


def init():
  testToString()
  testFromString()

def testToString():
  assertEquals("foo", strings.toString("foo"))
  assertEquals("5", strings.toString(5))
  assertEquals("5.5", strings.toString(5.5))
  assertEquals("True", strings.toString(True))
  assertEquals("False", strings.toString(False))
  assertEquals("foobarbaz", strings.toString(["foo", "bar", "baz"]))
  assertEquals("foo;bar;baz", strings.toString(("foo", "bar", "baz"), ";"))
  assertEquals("foo|bar|baz", strings.toString({"foo": 1, "bar": 2, "baz": 3}, "|"))

def testFromString():
  assertTrue(strings.boolFromString("trUe"))
  assertFalse(strings.boolFromString("fALSE"))
  assertFalse(strings.boolFromString("foo"))
  assertFalse(strings.boolFromString("0"))
  assertTrue(strings.boolFromString("1"))
  assertTrue(strings.boolFromString("-1"))
  assertFalse(strings.boolFromString("0.0"))
  assertTrue(strings.boolFromString("0.1"))
  assertTrue(strings.boolFromString("-0.1"))

  assertEquals(5, strings.intFromString("5"))
  assertEquals(5,  strings.intFromString("5.5"))
  assertEquals(-5, strings.intFromString("-5"))
  assertEquals(-5, strings.intFromString("-5.5"))
  assertNone(strings.intFromString("f"))

  assertEquals(5,  strings.floatFromString("5"))
  assertEquals(5.5, strings.floatFromString("5.5"))
  assertEquals(-5, strings.floatFromString("-5"))
  assertEquals(-5.5, strings.floatFromString("-5.5"))
  assertNone(strings.floatFromString("f"))

  assertEquals(["foo"], strings.listFromString("foo"))
  assertEquals(["foo", "bar", "baz"], strings.listFromString("foo;bar;baz"))
  assertEquals(["foo;bar;baz"], strings.listFromString("foo;bar;baz", sep="|"))
  assertEquals(["foo", "bar", "baz"], strings.listFromString("foo|bar|baz", sep="|"))
  assertEquals(["foo;bar", "baz"], strings.listFromString("foo;bar|baz", sep="|"))
  assertEquals(["0", "1", "2", "3.5"], strings.listFromString("0;1;2;3.5"))
  assertEquals([0, 1, 2, 3], strings.listFromString("0;1;2;3.5", _type=int))
  assertEquals([0, 1, 2, 3.5], strings.listFromString("0;1;2;3.5", _type=float))
  assertEquals([True, False, True], strings.listFromString("True;False;True", _type=bool))
  assertEquals([True, False, True], strings.listFromString("True;0;1", _type=bool))
  assertEquals([False, True, True], strings.listFromString("False;-1;3.5", _type=bool))
  assertNone(strings.listFromString("foo;bar;baz", _type=int))

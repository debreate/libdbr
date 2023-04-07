
# ****************************************************
# * Copyright © 2023 - Jordan Irwin (AntumDeluge)    *
# ****************************************************
# * This software is licensed under the MIT license. *
# * See: LICENSE.txt for details.                    *
# ****************************************************

# string handling


## Convert an object to string.
#
#  @param obj
#    Object to be converted.
#  @param sep
#    Separation delimiter in case of obj being a list type.
#  @return
#    String containing string representations of vales in list.
def toString(obj, sep=""):
  res = ""
  if type(obj) in (list, tuple, dict):
    for i in obj:
      if res:
        res += sep
      res += str(i)
  else:
    res = str(obj)
  return res


__sstyles = {
  "end": 0,
  "bold": 1,
  "faint": 2,
  "em": 3,
  "ital": 3,
  "under": 4,
  "sblink": 5,
  "rblink": 6,
  "invert": 7,
  "conceal": 8,
  "xout": 9,
  "pfont": 10,
  "fraktur": 20,
  "dunder": 21,
  "bold-off": 22,
  "faint-off": 22,
  "em-off": 23,
  "ital-off": 23,
  "fraktur-off": 23,
  "under-off": 24,
  "blink-off": 25,
  # 26?
  "invert-off": 27,
  "conceal-off": 28,
  "xout-off": 29,
  # 38 TODO: set custom color with '5;<n>' or '2;<r>;<g>;<b>'
  "fg-off": 39,
  # 48 TODO: same as 38
  "bg-off": 49,
  # 50?
  "frame": 51,
  "circle": 52,
  "over": 53,
  "frame-off": 54,
  "circle-off": 54,
  "over-off": 55
  # more?
}

for _idx in range(1, 10):
  __sstyles["afont{}".format(_idx)] = _idx + 10
for _idx in range(1, 9):
  __sstyles["fg{}".format(_idx)] = _idx + 29
for _idx in range(1, 9):
  __sstyles["bg{}".format(_idx)] = _idx + 39

## Formats a stylized string for terminal output.
#
#  @param st
#    String to be formatted.
#  @return
#    String formatted using ANSI escape codes (Select Graphic Rendition).
def sstyle(st):
  for key in __sstyles:
    st = st.replace("<{}>".format(key), "\033[{}m".format(__sstyles[key]))
  return st

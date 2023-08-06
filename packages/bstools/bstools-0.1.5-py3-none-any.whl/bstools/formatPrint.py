#! /usr/bin/env python3
#! coding='utf-8' 

from enum import Enum
import sys

class LftColor(Enum):
    black = 30
    red = 31
    green = 32
    yello = 33
    blue = 34
    purple = 35
    cyanine = 36
    white = 37
    
class LbgColor(Enum):
    black = 40
    red = 41
    green = 42
    yello = 43
    blue = 44
    purple = 45
    cyanine = 46
    white = 47
    
class LsType(Enum):
    defute = 0
    highlight = 1
    underLine = 4
    blink = 5
    reverse = 7
    disable = 8

def cprint(info, f = 0, a = 0, t = 0):
    fortString = "\033[%s%s%sm"%(
        str(t.value) + ";" if t else "", 
        str(f.value) + ";"if f else "", 
        a.value if a else ""
    )
    afterString = "\033[0m"
    if sys.platform != "win32":
        print("%s%s%s"%(fortString, info, afterString)[:-1])
    else:
        print("%s"%info[:-1])
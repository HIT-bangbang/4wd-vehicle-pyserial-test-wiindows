from ctypes.wintypes import CHAR


# coding=utf-8

from ctypes import *
print(c_char(170))
print(chr(170).encode().hex())
print(chr(0xaa).encode("utf-8"))
print(CHAR(170))


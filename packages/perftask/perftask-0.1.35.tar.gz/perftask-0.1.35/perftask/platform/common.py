import sys
from sys import platform as sys_platform

PY3 = sys.version_info >= (3, 0)

if sys_platform == "linux" or sys_platform == "linux2":
    OS = "linux"
elif sys_platform == "darwin":
    OS = "osx"
elif sys_platform == "win32":
    OS = "windows"


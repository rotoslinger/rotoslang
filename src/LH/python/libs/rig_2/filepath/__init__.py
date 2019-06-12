import time, os, fnmatch, shutil, sys, os
OPERATING_SYSTEM = sys.platform
def get_delimeter():
    delimeter = "/"
    if OPERATING_SYSTEM == "win32" or OPERATING_SYSTEM == "win64":
        delimeter =  "\\"
    return delimeter

DELIMETER = get_delimeter()
import sys

#Create os-independent interface for paths and os-specific functions
platform = sys.platform()
if platform == "linux" or platform == "linux2":
    # linux
    from linux import *
elif platform == "darwin":
    # OS X
    print("Not Supported")
    sys.exit()
elif platform == "win32":
    # Windows
    from windows import *
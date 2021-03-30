import tkinter as tk
from tkinter import *
import webbrowser
from tkinter.filedialog import askdirectory
from pytube import YouTube  # pip3 install pytube3
import getpass
from tkinter import messagebox
from ruamel import yaml
import os
import tkinter.font as tkFont
from pytube.exceptions import *
import time
import wget
import sys


#Create os-independent interface for paths and os-specific functions
os = sys.platform()
if platform == "linux" or platform == "linux2":
    # linux
    from linux import functions, paths
elif platform == "darwin":
    # OS X
    print("Not Supported")
    sys.exit()
elif platform == "win32":
    # Windows
    from windows import functions, paths

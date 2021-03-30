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

import os_spec


class App:
    def __init__(self):
        self.audioBool = False
        self.videoBool = False
        self.changedDefaultDir = bool
        self.path = os_spec.paths.desktop
        self.videoRes = False

        #Database
        self.fileLoc = os_spec.paths.fileLoc

        self.payload = [
            {
                'Options': {
                    'defaultDir': os_spec.paths.desktop,
                    'errorChoice': True,
                    'changedDefaultDir': False
                }
            }
        ]
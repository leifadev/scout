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

        #Generate initial yml file
        self.ymldir = os_spec.paths.ymldir

        config_folder_exists = True if os.path.exists(self.fileLoc) else False        
        yml_config_exists = True if os.path.isfile(self.ymldir) else False
        logo_exists = True if os.path.isfile() else False

        if config_folder_exists:
            print("Config folder found!")

            if yml_config_exists:
                print("Config file found!")
            else:
                print("Creating settings.yml,\nThis is not a restored version of a previously deleted one!")
                os.chdir(self.fileLoc)
                f = open("settings.yml","w+")
                f.close
                yaml.dump(self.payload, f, Dumper=yaml.RoundTripDumper)
        else:
            path = os.path.join(self.fileLoc)
            os.makedirs(path, exist_ok=True)

        if logo_exists:
            print("Logo found!")
        else:
            print("Downloading logo .gif!")
            wget.download(os_spec.path.logo_url, os_spec.path.logo_loc)
            print("Download successful!")
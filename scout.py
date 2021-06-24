import tkinter as tk # main gui framework
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk,THEMES # dark mode theme and stuff
from PIL import Image, ImageTk
import tkinter.font as tkFont
import webbrowser
import pytube
import getpass
from ruamel import yaml
import os
import wget
import ssl
from sys import platform as _platform
import subprocess # used for ffmpeg (file formatting)
import shutil # mainly used for detecting ffmpeg installation
from datetime import datetime
import time
from zipfile import ZipFile
from urllib.error import HTTPError


class App:
    def __init__(self, root):

        # Iniatiating variables for all sorts of stuff
        self.audioBool = False
        self.videoBool = False
        self.changedDefaultDir = bool
        self.thumbBool = bool
        self.videoRes = False
        self.hasFilePrefix = True
        self.filePrefix = ""
        ssl._create_default_https_context = ssl._create_unverified_context
        self.path = ""
        self.darkMode = False
        self.maxModeUse = 0
        self.version = "v1.5"
        self.logFont = "No value!"
        self.getUser = getpass.getuser()
        self.videoq = "" # vid quality example: 720p
        self.audioq = "" # audio quality example: 128kbs
        self.videof = "" # vid format example: mp4
        self.audiof = "" # audio format example: wav
        # DEVS DONT INCLUDE "."s ^^^BEFORE EXTENSIONS^^^


        ####################################################
        #                                                  #
        #             Backend Config and Logos             #
        #                                                  #
        ####################################################

        # Sets various variables for each OS being used.
        # Fonts, directories, special boolean values, etc.
        if _platform in ("linux", "linux2"):
            self.fileLoc = os.path.expanduser("~/.config/Scout/")
            self.dirDefaultSetting = "/home/" + self.getUser + "/Desktop"
            self.ymldir = os.path.expanduser("~/.config/Scout/settings.yml")
            self.cachedir = os.path.expanduser("~/.config/Scout/cache.yml")
            if self.path ==  "":
                self.path = "/home/" + self.getUser + "/Desktop"
            else:
                print("You don't have a selected path! Defaulting your desktop.\nFor more help use the help button to our github.")
            self.restartMsgY = None
            self.path_slash = "/"
            self.UIAttributes = { # dictionarys for each OS to match aesthics
                "Font": "Source Code Pro",
                "charSize": 10,
                "restartTextPos": 308,
                "logFont": "Courier",
                "logSize": 8
            }

        elif _platform == "darwin":
            self.fileLoc = "/Users/" + self.getUser + "/Library/Application Support/Scout/"
            self.dirDefaultSetting = "/Users/" + self.getUser + "/Desktop"
            self.cachedir = "/Users/" + self.getUser + "/Library/Application Support/Scout/cache.yml"
            self.ymldir = "/Users/" + self.getUser + "/Library/Application Support/Scout/settings.yml"
            if self.path ==  "":
                self.path = "/Users/" + self.getUser + "/Desktop"
            else:
                print("You don't have a selected path! Defaulting your desktop.\nFor more help use the help button to our github.")
            self.restartMsgY = None
            self.path_slash = "/"
            self.UIAttributes = { # dictionarys for each OS to match aesthics
                "Font": "Source Code Pro",
                "charSize": 12,
                "restartTextPos": 302,
                "logFont": "Source Code Pro",
                "logSize": 10
            }

        elif _platform in ("win64", "win32"):
            self.fileLoc = "C:\\Users\\" + self.getUser + "\\Appdata\\Roaming\\Scout\\"
            self.dirDefaultSetting = "C:\\Users\\" + self.getUser + "\Desktop"
            self.ymldir = "C:\\Users\\" + self.getUser + "\\AppData\\Roaming\\Scout\\settings.yml"
            self.cachedir = "C:\\Users\\" + self.getUser + "\\AppData\\Roaming\\Scout\\cache.yml"
            if self.path ==  "":
                self.path = "C:\\Users\\" + self.getUser + "\Desktop"
            else:
                print("You don't have a selected path! Defaulting your desktop.\nFor more help use the help button to our github.")
            self.restartMsgY = None
            self.path_slash = "\\"
            self.UIAttributes = { # pre-made attributes to be place holders for multiple tkinter parames later on
                "Font": "Courier",
                "charSize": 8,
                "restartTextPos": 302,
                "logFont": "Courier",
                "logSize": 8
            }



        ####################################################
        ### Updating and Restoring YML settings initally ###
        ####################################################

        # Summary of this block: This generates the YML from scratch if its outdated or doesnt exist, and ignores otherwise.
        # Uses sample yml "cache.yml" to compare it being the newest yml to a potentially old one. (Not ennough or different settings).

        # Pre-made Database (pre-made yml structure for intial generation)
        self.payload = [
            {
                'Options': {
                    'defaultDir': self.dirDefaultSetting,
                    'errorChoice': True,
                    'changedDefaultDir': False,
                    'hasFilePrefix': self.hasFilePrefix,
                    'darkMode': self.darkMode,
                    'thumbnail': False
                }
            }
        ]

        # Generates initial yml file and folder, detects missing files as well
        if not os.path.isfile(self.fileLoc):
            path = os.path.join(self.fileLoc)
            print(os.getcwd())
            os.makedirs(path, exist_ok=True)
            print("Folder generated...")
        if not os.path.isfile(self.ymldir) or os.path.getsize(self.ymldir) == 0:
                print("Creating the settings.yml,\nThis is NOT a restored version of a previously deleted one!")
                os.chdir(self.fileLoc)
                print(os.getcwd())
                f = open("settings.yml","w+")
                f.close
                yaml.dump(self.payload, f, Dumper=yaml.RoundTripDumper)
                print("if statement passes")
        # makes a copy of the newest yml/settings structure
        os.chdir(self.fileLoc)
        cache = open("cache.yml", "w+")
        cache.close
        yaml.dump(self.payload, cache, Dumper=yaml.RoundTripDumper)
        print("Cache updated!")


        # updating yml if is outdated with options (based on amount of keys)
        # It basically fetches all current yml values and compares them to a clean new copy for the supposed newest installed version,
        # If it find differences it will reset the settings to apply a new config.
        ## Dev note: I can make this not reset everything, I can code it differently and/or use ruamel.yaml to fix this
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            with open(self.cachedir) as cache:
                cacheData = yaml.load(cache, Loader=yaml.Loader)
                settingsList = []
                cacheList = []
                for x in data[0]['Options']:
                    settingsList.append(x)
                for y in cacheData[0]['Options']:
                    cacheList.append(y)
                # print(f'\nCurrent Detect YML Options:\nSettings: {settingsList}\nCache: {cacheList}\n')
                # Checking if the newest YML is compatible, seeing a possibly older config, then updating it completely
                if settingsList == cacheList:
                    print("Your settings.yml is up to date!\n")
                else:
                    with open(self.ymldir, "w+") as yml:
                        data = yaml.load(yml, Loader=yaml.Loader)
                        os.chdir(self.fileLoc)
                        cache = open("cache.yml", "w+")
                        cache.close
                        yaml.dump(self.payload, yml, Dumper=yaml.RoundTripDumper)
                        print("Cache updated!")


        # Organizing and downloading app icon for each OS #
        # Building scout on windows with Pyinstaller needs the .ico file for use at first!

        print("Attemping logo downloading...")
        url = "https://raw.githubusercontent.com/leifadev/scout/main/scout_logo.png"

        # Download icon for use if not present
        if not os.path.isfile(self.fileLoc + "scout_logo.png"):
            wget.download(url, self.fileLoc + "scout_logo.png")
        self.icon = PhotoImage(file=self.fileLoc + "scout_logo.png")


        ####################################################
        #                                                  #
        #            UI Elements and Attributes            #
        #                                                  #
        ####################################################


        ## Attributes ##

        root.title("Scout")
        root.tk.call('wm', 'iconphoto', root._w, self.icon)

        width=845
        height=350
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        style = ttk.Style()

        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.darkMode = data[0]['Options']['darkMode']
            if self.darkMode:
                root.set_theme("equilux")
            else:
                if _platform == "darwin":
                    root['bg'] = "#ececec"
                    print("\nLaunching in light mode!")
                elif _platform == "linux" or _platform == "linux2":
                    root['bg'] = "#ececec"
                    print("\nLaunching in light mode!")


        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # DEPRECATED \/\/\/
        ## area where clicks are detected ##

#        frame = Frame(root, width=100, height=30)
#        frame.bind("<Button-1>", leftclick)
#        frame.place(x=170,y=300,width=35)
#        if self.darkMode:
#            frame["bg"] = '#464646'
#        else:
#            frame['bg'] = "#ececec"


#        canvas = Canvas(frame, width=845, height=350)
#        canvas.pack()
#
#        test = PhotoImage(file="test.png")
#        canvas.create_image(350,50,image=test)


        ## Menu items ##

        menubar = Menu(root)
        filemenu = Menu(menubar)
        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="Cut", accelerator="Command+X", command=lambda: root.focus_get().event_generate('<<Cut>>'))

        filemenu.add_command(label="Copy", accelerator="Command+C", command=lambda: root.focus_get().event_generate('<<Copy>>'))

        filemenu.add_command(label="Paste", accelerator="Command+V", command=lambda: root.focus_get().event_generate('<<Paste>>'))
        filemenu.add_command(label="Select All", accelerator="Command+A", command=lambda: root.focus_get().select_range(0, 'end'))

        filemenu.add_separator()

        filemenu.add_command(label="Exit", accelerator="Command+Q", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar)
        helpmenu.add_command(label="About", command=self.about_button)
        helpmenu.add_command(label="Help", command=self.helpButton_command)

        helpmenu.add_separator()

        helpmenu.add_command(label="Settings", command=self.settings_button)
        menubar.add_cascade(label="About", menu=helpmenu)

        root.config(menu=menubar)
        root.update()   # Updates window at startup to be interactive and lifted, DO NOT TOUCH


        ## Elements ##

        root.lift() # lift window to the top

        self.urlfield = ttk.Entry(root)
        self.urlfield["justify"] = "left"
        self.urlfield["text"] = ""
        self.urlfield.insert(0, '')   # add pre made message
        self.urlfield.place(x=20,y=60,width=540)


        self.downloadButton=ttk.Button(root)
#        self.downloadButton["justify"] = "center"
        self.downloadButton["text"] = "Download"
        self.downloadButton.place(x=570,y=59,width=120)
        self.downloadButton["command"] = self.downloadButton_command


        self.browseButton=ttk.Button(root)
        self.browseButton["text"] = "File Destination"
        self.browseButton["command"] = self.browseButton_command
        self.browseButton.place(x=690,y=59,width=140)


        self.videoButton=tk.Checkbutton(root)
        self.videoButton["text"] = "Video"
        self.videoButton.place(x=730,y=130,width=70,height=30)
        self.videoButton["offvalue"] = False
        self.videoButton["onvalue"] = True
        self.videoButton["command"] = self.videoButton_command

        self.audioButton=tk.Checkbutton(root)
        self.audioButton["text"] = "Audio"
        self.audioButton.place(x=730,y=190,width=70,height=30)
        self.audioButton["offvalue"] = False
        self.audioButton["onvalue"] = True
        self.audioButton["command"] = self.audioButton_command

        helpButton=ttk.Button(root)
        helpButton["text"] = "Help"
        helpButton.place(x=20,y=300,width=70)
        helpButton["command"] = self.helpButton_command

        clearButton=ttk.Button(root)
        clearButton["text"] = "Clear"
        clearButton.place(x=95,y=300,width=70)
        clearButton["command"] = self.clearConsole_command

        self.modeButton=ttk.Button(root)
        self.modeButton.place(x=170,y=300,width=100)
        self.modeButton["command"] = self.switchMode

        self.versionText = tk.Label(root)
        self.versionText = Label(root, text=self.version)
        self.versionText.place(x=795,y=300,width=40,height=25)
        self.versionText["font"] = tkFont.Font(family=self.UIAttributes.get("Font"), size=self.UIAttributes.get("charSize"))


        ## All selections/menus for format and quailty choice ##

        self.clickedvf = StringVar()
        self.clickedvf.set("mp4")
        self.videoformat = ttk.OptionMenu(root, self.clickedvf, "mp4", "mp4", "mov", "webm")
        # self.videoformat.place(x=650, y=121, width=70, height=30)
        self.videoformat["state"] = "normal"


        self.clickedaf = StringVar()
        self.clickedaf.set("mp4")
        self.audioformat = ttk.OptionMenu(root, self.clickedaf, "mp3", "mp3", "wav", "ogg")
        # self.audioformat.place(x=650, y=171, width=70, height=30)
        self.audioformat["state"] = "normal"

        self.clickedvq = StringVar()
        self.clickedvq.set("Quality")
        self.videoquality = ttk.OptionMenu(root, self.clickedvq, "Quality", "1080p", "720p", "480p", "360p", "240p", "144p")
        self.videoquality["state"] = "normal"

        self.clickedaq = StringVar()
        self.clickedaq.set("Quality")
        self.audioquality = ttk.OptionMenu(root, self.clickedaq, "Quality", "160kbs", "128kbs", "70kbs", "50kbs")
        self.audioquality["state"] = "normal"


        # Block of code to switch bgs and fgs manually for darkMode using only tk not ttk
        if self.darkMode:
            self.versionText["bg"] = "#464646" # dark theme gray
            self.versionText["fg"] = "#ececec" # light theme gray

            self.audioButton["bg"] = "#464646"
            self.videoButton["bg"] = "#464646"

            self.audioButton["fg"] = "#ececec"
            self.videoButton["fg"] = "#ececec"

        else:
            self.versionText['bg'] = "#ececec"
            self.versionText["fg"] = "#464646"

            #background color for Checkbuttons
            self.audioButton["bg"] = "#ececec"
            self.videoButton["bg"] = "#ececec"




        # Logfield #
        # Comes with error handling, video info, system/scout info/errors

        self.logfield = tk.Text(root)
        self.logfield.place(x=20,y=100,width=540, height=180)
        ft = tkFont.Font(family=self.UIAttributes.get("logFont"), size=self.UIAttributes.get("logSize"))
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(END, "Scout launched successfully!\nVersion: " + self.version + "\n")
        self.logfield["state"] = "disabled"
        if self.darkMode:
            self.logfield["bg"] = "#e5e5e5"
        else:
            self.logfield["bg"] = "#f6f6f6" # if you want change this into 1 line for a bg dont keep it there for future adjustments

        # Loading dark mode value from settings.yml for inital launch
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.enablePrompts = data[0]['Options']['errorChoice']
            self.darkMode = data[0]['Options']['darkMode']
            if self.darkMode:
                self.modeButton["text"] = "Light Mode"
            else:
                self.modeButton["text"] = "Dark Mode"


    #############################################################################


    ## Triggers and Scripts ##
    # These coinside with the log field element itself

    # FFmpeg warning: For formatting one must install ffmpeg for video formatting
        self.ffmpeg = bool

        if _platform != "darwin":
            if shutil.which('ffmpeg') is None:
                self.logfield["state"] = "normal"
                self.logfield.insert(END, f'\nWARNING: You do not have FFmpeg installed, and you cannot choose custom file types!\n |\n └ MacOS: Install homebrew and download it, "brew install ffmpeg". Install brew from \nhttps://brew.sh\n | \n └ Linux: Install it with your package manager, e.g. apt install ffmpeg.\n | \n └ Windows: Install it through http://ffmpeg.org. If it is installed, make sure that the folder of the ffmpeg executable is on the PATH.\n')
                self.ffmpeg = False
                self.logfield["state"] = "disabled"
                print("You don't have FFmpeg installed! You can't use custom file types.")
                # Disable menus that require ffmpeg
                self.audioquality["state"] = "disabled"
                self.videoquality["state"] = "disabled"
                self.videoformat["state"] = "disabled"
                self.audioformat["state"] = "disabled"
                print("\nFFmpeg isn't installed, read console for instructions!\n")
            else:
                self.ffmpeg = True
                print("\nYou have FFmpeg installed! You can use custom file types.\n")
        else:
            self.logfield["state"] = "normal"
            if not os.path.isfile(self.fileLoc + "ffmpeg"):
                messagebox.showwarning("Warning", "You do not have FFmpeg library installed, please wait several seconds for it to install.\n\nInternet is required!")

                self.logfield["state"] = "normal"

                self.logfield.insert(END, f'\nINFO: If don\'t have an internet connection to isntall FFmpeg, you can for now use file formatting features.\n\nJust relaunch scout when you have internet and you are good to go.\n\nPlease go to the help button and to seek guidance on the wiki and more.')

                print("\nYou don\'t have FFmpeg installed! DONT WORRY, it will be installed automatically for you now!\n")

                os.chdir(self.fileLoc)
                wget.download("https://evermeet.cx/ffmpeg/getrelease/zip", self.fileLoc + "ffmpeg.zip")

                print("\nDownloading latest stable version of ffmpeg, may take several seconds!\n")

                with ZipFile("ffmpeg.zip", 'r') as zip: # extracts downloaded zip from ffmpegs download API for latest release
                    zip.extractall()
                print("\nFile extracted...\n")

                subprocess.run(f"chmod 755 \"ffmpeg\"", shell=True) # gives perms for the file to be an executable like all binaries should be
                print("\nFFmpeg binary is now executable! :)\n")

                os.remove("ffmpeg.zip") # remove zipped file for clean dir and less space
                print("\nPurged inital zip file\n")

                print("\nFFmpeg was sucessfully automatically installed to your config directory!\n")

                messagebox.showinfo("Success!", "FFmpeg was installed! Continue.")

            if os.path.isfile(self.fileLoc + "ffmpeg"): # chevck again if it is now installed
                print("\nFFmpeg is present in your config folder!\n(" + self.fileLoc + ")\n")
                self.ffmpeg = True
            else: # If the binary file still isnt present after the first if block which downloads/installs it
                print("\n----!!\nCould not find the ffmpeg binary (your source to convert files and more) in your config \ndirecotry after attempting to install it for you. \n\n**Please** contact the developer if you see this message in an issue on github preferabley!\n----!!\n")
                self.logfield.insert(END, f'\nINFO: Could not find the ffmpeg binary (your source to convert files and more) in your config \ndirecotry after attempting to install it for you. \n\nYou can STILL USE SCOUT but without file formatting features.')
                self.audioquality["state"] = "disabled"
                self.videoquality["state"] = "disabled"
                self.videoformat["state"] = "disabled"
                self.audioformat["state"] = "disabled"
                self.ffmpeg = False
            self.logfield["state"] = "disabled"


    ######################################################################################


    def videoFetch(self, yt, query): # Basic video basic report (used in all download types)
        yt = YouTube(query)
        query = self.urlfield.get()
        self.logfield.insert(END, f'\n---------------------------------------------------------------------')
        self.logfield.insert(END, f'\n\nStarting download to path: {self.path}')
        self.logfield.insert(END, f'\nVideo Title: {yt.title}')
        self.logfield.insert(END, f'\nVideo Author: {yt.author}')
        self.logfield.insert(END, f'\nPublish Date: {yt.publish_date}')
        self.logfield.insert(END, f'\nVideo Duration (sec): {yt.length}')
        self.logfield.insert(END, f'\nViews: {yt.views}')
        self.logfield.insert(END, f'\nRating ratio: {yt.rating}')
        self.logfield.insert(END, f'\n\n---------------------------------------------------------------------\n\n')

        self.logfield["state"] = "disabled" # quickly disbaled user ability to edit log after done inserting


    ## Quality choices
    # Video: 144p 240p 360p 720p 1080p
    # Audio: 24, 64, 96, 128, 192kbps

    # self.videoq = "720p"
    # self.audioq = "128kbps"

    ## Format choices
    # Video: mp4, mov
    # Audio: mp3, wav, ogg

    # self.videof = "mp4"
    # self.audiof = "mp3"

    # ffmpeg -hide_banner -loglevel error -y -i xboxyay.mp3 xboxyayyy.wav

    # Download buttons scripting, includes all features said abive

    def downloadButton_command(self): # quite a big function ;)

        error_dict = { # All errors stored in this dictionary to be called later for more clear code
        'VideoPrivate': "\nERROR: This video is privated, you can't download it\n",
        'RegexMatchError': "\nERROR: Invalid link formatting\n",
        'VideoRegionBlocked': '\nERROR: This video is block in your region\n',
        'RecordingUnavailable': "\nERROR: This recording is unavalilable\n",
        'MembersOnly': "\nERROR: This video is for channel members only.\nRefer here for more info: https://support.google.com/youtube/answer/7544492\n",
        'LiveStreamError': "\nERROR: This is a livestream, and not a downloadable video\n",
        'HTMLParseError': "\nERROR: HTML parsing or extraction has failed",
        'VideoUnavailable': "\nERROR: This video is unavalilable, may possibly be payed material or region-locked\n"}

        try:
            try:
                self.logfield["state"] = "normal"

                query = self.urlfield.get() # gets entry input
                yt = YouTube(query)


            except RegexMatchError:
                print("Regex match error! Invalid...")


            with open(self.ymldir, "r") as yml:
                data = yaml.load(yml, Loader=yaml.Loader)
                self.thumbBool = data[0]['Options']['thumbnail']
                if self.thumbBool:
                    wget.download(yt.thumbnail_url, self.path + "/" + self.filePrefix + yt.title + ".jpg")
                    print("\nDownloading the thumbnail as well :) \nIf your seeing this and your thumbnail setting is off, please delete your config file and restart scout.\nConfig file path: " + self.ymldir + "\n")

            if self.videoBool and self.audioBool: # Video and Audio
                self.logfield["state"] = "normal"
                try:
                    yt = YouTube(query)
                    res = self.clickedvq.get()
                    # This block searches through a dictionary of known quality values, then suggests available values later
                    streams = str(yt.streams.filter(progressive=True).all())
                    attributes = {
                        "res": ["1080p", "720p", "480p", "360p", "240p", "144p"],
                        "fps": [24, 30, 60]
                    }
                    aRes = []
                    aFPS = []
                    for key in attributes: # Looping through "attributes" and "streams" to match available ones
                        for i in attributes.get(key):
                            if str(i) in str(streams):
                                if key == "res":
                                    aRes.append(i) # Put into a list to be printed later
                                else:
                                    aFPS.append(i)
                    try:
                        if self.clickedvq.get() == "Quality":
                            res = aRes[0]
                        # elif self.clickedvfps.get() == "Fps":
                        #     fps = aFPS[0]
                    except:
                        print("\nNo other available values were found to fallback on, check for any stream query objects above!")

                    videoDown = yt.streams.filter(res=res, progressive=True).first()
                    print(res)
                    print(f'\nAvailable stream(s):\n{videoDown}', f'All streams:\n{streams}')

                    # Block that converts custom file types, video/audio #

                    if videoDown == None: # This tiny block for error handling no known download settings, suggests them afterwards
                        self.logfield.insert(END, f'\nERROR: This video is unavailable with these download settings!\n')

                        print("Gathered available quality options: ", aRes) # extra verbose input
                        suggestMsg = f'\nINFO: Try the {aRes} resolutions instead\n'
                        self.logfield.insert(END, f'{suggestMsg}') # Suggest available values from aRes/aFPS

                        self.logfield["state"] = "disabled"
                        return

                    if self.clickedvf.get() != "mp4": # see if selected file types aren't the default and therefore need to be converted
                        videoDown.download(self.fileLoc, filename_prefix=self.filePrefix)
                        os.chdir(self.fileLoc)
                        # From below we mod the downloaded file for perms to be used with, UNIX system only apply
                        self.logfield.insert(END, f'\n---------------------------------------------------------------------\nINFO: Modding file permissions...\n')
                        filtered = yt.title.translate({ord(i): None for i in '|;:/"\',.?*^%$#'}) # filter fetched yt title and remove all special chars, as pytube removes them when it downloads the first one we need to mod
                        subprocess.run(f"chmod 755 \"{filtered}.mp4\"", shell=True) # give perms for file with ffmpeg
                        self.logfield.insert(END, f'\nINFO: Converting inital file to .{self.clickedvf.get()}\n')

                        # Running ffmpeg in console with subprocess, multiple flags to leave out extra verbose output from ffpmeg, and say yes to all arguments
                        subprocess.run(f'ffmpeg -hide_banner -loglevel error -y -i \"{self.fileLoc}{filtered}.mp4\" \"{self.path}{self.path_slash}{filtered}.{self.clickedvf.get()}\"', shell=True)

                        self.logfield.insert(END, f'\nINFO: Removing temp file...\n')
                        os.remove(f"{filtered}.mp4")

                        print("Original file deleted! Enjoy your converted one")

                        self.logfield.insert(END, f'\nINFO: The {videoDown}, codec/itag was used.\n') # This and below show in the log what actually stream object they downloaded with there video. Helpful for debugging!
                        self.videoFetch(yt, query) # Fetching post-log video info, function up top this download function
                    else:
                        videoDown.download(self.path, filename_prefix=self.filePrefix)
                        self.logfield.insert(END, f'\nINFO: The {videoDown}, codec/itag was used.\n')
                        self.videoFetch(yt, query)

                    self.videoFetch(yt, query)
                    self.logfield["state"] = "disabled"

                # Try statments using pytube errors repeats for each selection mode of video
                except VideoPrivate:
                    self.logfield.insert(END, error_dict.get('VideoPrivate'))
                except RegexMatchError:
                    self.logfield.insert(END, error_dict.get('RegexMatchError'))
                except RecordingUnavailable:
                    self.logfield.insert(END, error_dict.get('RecordingUnavailable'))
                except MembersOnly:
                    self.logfield.insert(END, error_dict.get('MembersOnly'))
                except LiveStreamError:
                    self.logfield.insert(END, error_dict.get('LiveStreamError'))
                except HTMLParseError:
                    self.logfield.insert(END, error_dict.get('HTMLParseError'))
                except VideoUnavailable:
                     self.logfield.insert(END, error_dict.get('VideoUnavailable'))
                self.logfield["state"] = "disabled"


            elif self.audioBool:  # Audio only
                self.logfield["state"] = "normal"
                try:
                    yt = YouTube(query)
                    audioDown = yt.streams.filter(abr=self.audioq, only_audio=True).first()
                    abr = self.clickedaq.get()
                    streams = str(yt.streams.filter(only_audio=True).all())
                    attributes = {
                        "abr": ["160kbs", "128kbs", "70kbs", "50kbs"]
                    }
                    aAbr = []
                    for key in attributes:
                        for i in attributes.get(key):
                            if str(i) in str(streams):
                                aAbr.append(i)

                    try:
                        if self.clickedvq.get() == "Quality":
                            abr = aAbr[0]
                    except:
                        print("\nNo other available values were found to fallback on, check for any stream query objects above!")

                    print(abr)
                    print(f'\nAvailable stream(s):\n{audioDown}', f'All streams:\n{streams}')

                    if audioDown == None: # This tiny block for error handling no known download settings, suggests them afterwards
                        self.logfield.insert(END, f'\nERROR: This video is unavailable with these download settings!\n')

                        print("Gathered available quality options: ", aAbr) # extra verbose input
                        suggestMsg = f'\nINFO: Try the {aAbr} resolutions instead\n'
                        self.logfield.insert(END, f'{suggestMsg}')

                        self.logfield["state"] = "disabled"
                        return

                    audioDown.download(self.fileLoc, filename_prefix=self.filePrefix)
                    os.chdir(self.fileLoc)
                    self.logfield.insert(END, f'\n---------------------------------------------------------------------\nINFO: Modding file permissions...\n')
                    filtered = yt.title.translate({ord(i): None for i in '|;:/,.?*^%$#"'})
                    subprocess.run(f"chmod 755 \"{filtered}.mp4\"", shell=True) # give perms for file with ffmpeg
                    self.logfield.insert(END, f'\nINFO: Converting inital file to .{self.clickedaf.get()}\n')
                    subprocess.run(f'ffmpeg -hide_banner -loglevel error -y -i \"{self.fileLoc}{filtered}.mp4\" \"{self.path}{self.path_slash}{filtered}.{self.clickedaf.get()}\"', shell=True)
                    self.logfield.insert(END, f'\nINFO: Removing temp file...\n')
                    os.remove(f"{filtered}.mp4")

                    print("Original file deleted! Enjoy your converted one")

                    self.logfield.insert(END, f'\nINFO: The {audioDown}, codec/itag was used.\n')

                    self.videoFetch(yt, query)
                    self.logfield["state"] = "disabled"

                # Try statments using pytube errors repeats for each selection mode of video
                except VideoPrivate:
                    self.logfield.insert(END, error_dict.get('VideoPrivate'))
                except RegexMatchError:
                    self.logfield.insert(END, error_dict.get('RegexMatchError'))
                except RecordingUnavailable:
                    self.logfield.insert(END, error_dict.get('RecordingUnavailable'))
                except MembersOnly:
                    self.logfield.insert(END, error_dict.get('MembersOnly'))
                except LiveStreamError:
                    self.logfield.insert(END, error_dict.get('LiveStreamError'))
                except HTMLParseError:
                    self.logfield.insert(END, error_dict.get('HTMLParseError'))
                except VideoUnavailable:
                     self.logfield.insert(END, error_dict.get('VideoUnavailable'))
                self.logfield["state"] = "disabled"


            elif self.audioBool == False and self.videoBool: # Video only
                self.logfield["state"] = "normal"
                if self.enablePrompts:
                    messagebox.showwarning("Warning", "Video resolutions for this option are lower quailty.")
                    self.logfield.insert(END, f'\nINFO: These downloads take extra long, don\'t quit me!\n')
                try:
                    yt = YouTube(query)
                    silent_audioDown = yt.streams.filter(res=self.videoq, only_video=True).first()
                    res = self.clickedvq.get()
                    streams = str(yt.streams.filter(only_video=True).all())
                    print(streams)
                    attributes = {
                        "res": ["1080p", "720p", "480p", "360p", "240p", "144p"]
                    }
                    aRes = []
                    for key in attributes:
                        for i in attributes.get(key):
                            if str(i) in str(streams):
                                aRes.append(i)

                    try:
                        if self.clickedvq.get() == "Quality":
                            res = aRes[0]
                    except:
                        print("\nNo other available values were found to fallback on, check for any stream query objects above!")

                    print(res)
                    print(f'\nAvailable stream(s):\n{silent_audioDown}', f'All streams:\n{streams}')

                    if silent_audioDown == None: # This tiny block for error handling no known download settings, suggests them afterwards
                        self.logfield.insert(END, f'\nERROR: This video is unavailable with these download settings!\n')

                        print("Gathered available quality options: ", aRes) # extra verbose input
                        suggestMsg = f'\nINFO: Try the {aRes} resolutions instead\n'
                        self.logfield.insert(END, f'{suggestMsg}')

                        self.logfield["state"] = "disabled"
                        return
                    if self.clickedvf != "mp4":
                        silent_audioDown.download(self.fileLoc, filename_prefix=self.filePrefix)
                        os.chdir(self.fileLoc)
                        self.logfield.insert(END, f'\n---------------------------------------------------------------------\nINFO: Modding file permissions...\n')
                        filtered = yt.title.translate({ord(i): None for i in '|;:/,.?*^%$#"'})
                        subprocess.run(f"chmod 755 \"{filtered}.mp4\"", shell=True) # give perms for file with ffmpeg
                        self.logfield.insert(END, f'\nINFO: Converting inital file to .{self.clickedvf.get()}\n')
                        subprocess.run(f'ffmpeg -hide_banner -loglevel error -y -i \"{self.fileLoc}{filtered}.mp4\" \"{self.path}{self.path_slash}{filtered}.{self.clickedvf.get()}\"', shell=True)
                        self.logfield.insert(END, f'\nINFO: Removing temp file...\n')
                        os.remove(f"{filtered}.mp4")

                        print("Original file deleted! Enjoy your converted one")

                        self.logfield.insert(END, f'\nINFO: The {silent_audioDown}, codec/itag was used.\n')
                    else:
                        silent_audioDown.download(self.path, filename_prefix=self.filePrefix)
                        self.logfield.insert(END, f'\nINFO: The {silent_audioDown}, codec/itag was used.\n')

                    self.videoFetch(yt, query)
                    self.logfield["state"] = "disabled"

                # Try statments using pytube errors repeats for each selection mode of video
                except VideoPrivate:
                    self.logfield.insert(END, error_dict.get('VideoPrivate'))
                except RegexMatchError:
                    self.logfield.insert(END, error_dict.get('RegexMatchError'))
                except RecordingUnavailable:
                    self.logfield.insert(END, error_dict.get('RecordingUnavailable'))
                except MembersOnly:
                    self.logfield.insert(END, error_dict.get('MembersOnly'))
                except LiveStreamError:
                    self.logfield.insert(END, error_dict.get('LiveStreamError'))
                except HTMLParseError:
                    self.logfield.insert(END, error_dict.get('HTMLParseError'))
                except VideoUnavailable:
                     self.logfield.insert(END, error_dict.get('VideoUnavailable'))
                self.logfield["state"] = "disabled"


            else:
                self.logfield["state"] = "normal" # disable log after any erros are detected

                query = self.urlfield.get() # gets entry input (the users specifed URL)

                if self.urlfield.get() == "":
                    self.logfield["state"] = "normal" # disable log after any erros are detected

                elif self.enablePrompts: # hasnt selected video nor audio
                    self.logfield.insert(END, f'\nERROR: You can\'t download a video with video or audio!\n')

                self.logfield["state"] = "disabled" # disabled the entirity again

        except HTTPError as err:
            self.logfield["state"] = "normal" # disable log after any erros are detected
            print("\n\nThere was a 404 Not Found error!\n" + str(err) + "\n")

            self.logfield.insert(END, f'\nERROR: There was a 404 Not Found error. Internet down?\nOtherwise may be a (temporary) bug on the backend.\n\nBring this to thr github.\n')
            self.logfield["state"] = "disabled" # disable log after any erros are detected


    ########################################################################################################

    # Button and toggle functions/commands/calls for main window

    def switchMode(self): # launches and toggles light and dark mode value
        print("Click event successful!")
        if self.darkMode == False:
            self.darkMode = True
            self.modeButton["text"] = "Light Mode"
        else:
            self.darkMode = False
            self.modeButton["text"] = "Dark Mode"

        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)

        with open(self.ymldir,"w+") as yml: # updates dark mode boolean to YML settings
            data[0]['Options']['darkMode'] = self.darkMode
            write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
            self.darkMode = data[0]['Options']['darkMode']
            print(self.darkMode)
        print("\nCurrently updating settings.yml...")

        # Stop more than 1 use for user to restart app, avoid spam clicking issues and such
        self.maxModeUse += 1
        if self.maxModeUse == 1:
            self.modeButton["state"] = "disabled"
            self.maxWarn = Label(root, text=self.version)
            if self.darkMode:
                self.maxWarn["fg"] = "#464646" # light theme gray
                self.maxWarn["bg"] = "#ececec"
            else:
                self.maxWarn["fg"] = "#ececec" # If statement checking if darkMode is on and to switch bg accordingly
                self.maxWarn["bg"] = "#464646"
            self.maxWarn.place(x=280,y=302,width=140)
            self.maxWarn["text"] = "Restart to apply!"
            self.maxWarn["font"] = tkFont.Font(family=self.UIAttributes.get("Font"), size=self.UIAttributes.get("charSize"))

    # This is function for the "File Destination" button in the main menu
    # Uses tkinter and fetches yml values to work
    def browseButton_command(self):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.path = data[0]['Options']['defaultDir'] # Fetch any set default directories specificed in settings pane

        if self.changedDefaultDir:
            askdirectory(initialdir=self.path)
        else:
            askdirectory(initialdir='/Users/' + self.getUser + '/Desktop/')

    # This includes changes boolean status for video/audio inclusion as well as handling the UI elements for them
    def videoButton_command(self):
        if self.videoBool == False:
            self.videoBool = True
            self.videoformat.place(x=650, y=160, width=75, height=30)
            self.videoquality.place(x=638, y=130, width=87, height=30)
            if self.audioBool:
                self.audioformat.place_forget()
                self.audioquality.place_forget()
        else:
            self.videoBool = False
            self.videoformat.place_forget()
            self.videoquality.place_forget()
            if self.audioBool:
                self.audioformat.place(x=655, y=220, width=70, height=30)
                self.audioquality.place(x=635, y=190, width=87, height=30)
        print("Video status: " + str(self.videoBool))


    # This includes changes boolean status for video/audio inclusion as well as handling the UI elements for them
    def audioButton_command(self):
        if self.audioBool == False:
            self.audioBool = True
            if self.videoBool == False:
                self.audioformat.place(x=650, y=220, width=75, height=30)
                self.audioquality.place(x=638, y=190, width=87, height=30)
        else:
            self.audioBool = False
            self.audioformat.place_forget()
            self.audioquality.place_forget()

        print("Audio status: " + str(self.audioBool))

    # Help button takes user the github page, has wiki, code,issues, readme.md file and more
    def helpButton_command(self):
        webbrowser.open("https://github.com/leifadev/scout")
        self.logfield["state"] = "normal"
        self.logfield.insert(END, "\nINFO: Launched help page! Documentation, Code, Wiki, and more :)\n")
        self.logfield["state"] = "disabled"
        print("This is opening the github page to for Scout. All versions of scout, a public wiki, and an issues page\nare there to help!")

    # Clear the whole test entry, deleting line until the end, still restarting the welcome message!
    def clearConsole_command(self):
        self.logfield["state"] = "normal"
        if self.enablePrompts:
            messagebox.showwarning("Warning", "Are you sure you want to clear the console?")
            self.logfield.delete("1.0","end")
            self.logfield.insert(END, "Scout launched successfully!\nVersion: " + self.version + "\n")
        else:
            self.logfield.delete("1.0","end")
            self.logfield.insert(END, "Scout launched successfully!\nVersion: " + self.version + "\n")
        self.logfield["state"] = "disabled" # quickly disbaled user ability to edit log


    #################################################################

    ## Settings pane ##

    def getTheme(self, name): # Dark mode enable fetching from settings YML
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.darkMode = data[0]['Options']['darkMode']
            if self.darkMode:
                name.set_theme("equilux")
            else:
                print("No theme! Light mode then...")
                name["bg"] = "#ececec"

    # About button UI and scripting
    def about_button(self):
        abt = ThemedTk(themebg=True)
        abt.iconbitmap = PhotoImage(file=self.fileLoc + "scout_logo.png")
        self.getTheme(abt)

        abt.title("About")
        width=300
        height=300
        screenwidth = abt.winfo_screenwidth()
        screenheight = abt.winfo_screenheight()
        abt_alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        abt.geometry(abt_alignstr)
        abt.resizable(width=False, height=False)

        # Top 'Settings' title text
        self.abtTitle = ttk.Label(abt)
        self.abtTitle = Label(abt, text="About")
        self.abtTitle.place(x=45,y=10,width=210)
        if self.darkMode:
            self.abtTitle["bg"] = "#464646" # dark theme gray
            self.abtTitle["fg"] = "#999999" # light theme gray
        else:
            self.abtTitle['bg'] = "#ececec"
            self.abtTitle["fg"] = "black"

        ## All below are just the elements to the about pane, you can figure these out I'm sure :)
        abtMsg = "Author: leifadev\nLicense: GPL/GNU v3\nVersion: " + self.version + "\n\nLanguage: Python 3\nCompilier: Pyinstaller\nFramework: Tkinter"
        self.msg = ttk.Label(abt)
        self.msg = Label(abt, text=abtMsg, anchor=CENTER, wraplength=160, justify=CENTER)
        self.msg.place(x=50,y=40,width=200)
        if self.darkMode:
            self.msg["bg"] = "#464646" # dark theme gray
            self.msg["fg"] = "#999999" # light theme gray
        else:
            self.msg['bg'] = "#ececec"
            self.msg["fg"] = "black" # If statement checking if darkMode is on and to switch bg accordingly


        self.abtLink = "Contribute to the wiki!"
        self.abtLink = ttk.Label(abt)
        self.abtLink = Label(abt, font=(self.UIAttributes.get("Font"), self.UIAttributes.get("charSize"), "underline"), text="Read the wiki for more info!", anchor=CENTER, wraplength=160, justify=CENTER)
        self.abtLink.place(x=50,y=170,width=200)
        self.abtLink["fg"] = "#2f81ed"
        self.abtLink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/leifadev/scout/wiki"))
        if self.darkMode: # If statement checking if darkMode is on and to switch bg accordingly
            self.abtLink["bg"] = "#464646" # dark theme gray
        else:
            self.abtLink['bg'] = "#ececec"

    # Settings pane UI and scripting
    def settings_button(self): # Settings pane, offers custiomizable features!

        sWin = ThemedTk(themebg=True)
        sWin.iconbitmap = PhotoImage(file=self.fileLoc + "scout_logo.png")

        self.getTheme(sWin)
        sWin.title("Settings")
        width=550
        height=400
        screenwidth = sWin.winfo_screenwidth()
        screenheight = sWin.winfo_screenheight()
        sWin_alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        sWin.geometry(sWin_alignstr)
        sWin.resizable(width=False, height=False)


        self.settingsTitle = ttk.Label(sWin)
        self.settingsTitle = Label(sWin, text="Settings")
        self.settingsTitle.place(x=207,y=10,width=140)
        if self.darkMode:
            self.settingsTitle["bg"] = "#464646" # dark theme gray
            self.settingsTitle["fg"] = "#999999" # light theme gray
        else:
            self.settingsTitle['bg'] = "#ececec"# If statement checking if darkMode is on and to switch bg accordingly
            self.settingsTitle["fg"] = "black"

        self.defaultDirButton=ttk.Button(sWin, text="Choose") # Disabled default dir until further notice
        self.defaultDirButton.place(x=287,y=50,width=120)
        self.defaultDirButton["command"] = self.defaultDir_command


        self.defaultDirTip = ttk.Label(sWin)
        self.defaultDirTip = Label(sWin, text="Set Default Directory")
        self.defaultDirTip.place(x=147,y=52,width=140)
        if self.darkMode:
            self.defaultDirTip["bg"] = "#464646" # dark theme gray
            self.defaultDirTip["fg"] = "#999999" # light theme gray
        else:
            self.defaultDirTip['bg'] = "#ececec"
            self.defaultDirTip["fg"] = "black"


        self.warnMenu = ttk.Button(sWin)
        self.warnMenu["text"] = "Toggle Off"
        self.warnMenu.place(x=292,y=92,width=110)
        self.warnMenu["command"] = self.errorToggle     #  toggle button for prompts lolz

        self.warnTip = ttk.Label(sWin)
        self.warnTip = Label(sWin, text="Recieve Prompts")
        self.warnTip.place(x=165,y=92,width=110)
        if self.darkMode:
            self.warnTip["bg"] = "#464646" # dark theme gray
            self.warnTip["fg"] = "#999999" # light theme gray
        else:
            self.warnTip['bg'] = "#ececec"
            self.warnTip["fg"] = "black"

        self.prefixMenu = ttk.Button(sWin)
        self.prefixMenu["text"] = "Toggle Off"
        self.prefixMenu.place(x=292,y=137,width=110)
        self.prefixMenu["command"] = self.togglePrefix   # SECOND

        self.prefixTip = ttk.Label(sWin)
        self.prefixTip = Label(sWin, text="File Prefix")
        self.prefixTip.place(x=165,y=137,width=110)
        if self.darkMode:
            self.prefixTip["bg"] = "#464646" # dark theme gray
            self.prefixTip["fg"] = "#999999" # light theme gray
        else:
            self.prefixTip['bg'] = "#ececec"
            self.prefixTip["fg"] = "black"


        self.thumbMenu = ttk.Button(sWin)
        self.thumbMenu["text"] = "Toggle Off"
        self.thumbMenu.place(x=292,y=181,width=110)
        self.thumbMenu["command"] = self.toggleThumb

        self.thumbTip = ttk.Label(sWin)
        self.thumbTip = Label(sWin, text="Get Thumbnail")
        self.thumbTip.place(x=165,y=181,width=120)
        if self.darkMode:
            self.thumbTip["bg"] = "#464646" # dark theme gray
            self.thumbTip["fg"] = "#999999" # light theme gray
        else:
            self.thumbTip['bg'] = "#ececec"
            self.thumbTip["fg"] = "black"


        self.resetDefaultDir = ttk.Button(sWin)
        self.resetDefaultDir["text"] = "Reset Default Directory"
        self.resetDefaultDir.place(x=200,y=235,width=180)
        self.resetDefaultDir["command"] = self.resetDefaultDir_command
        self.resetDefaultDir["state"] = "normal"

        self.resetDirTip = ttk.Label(sWin)
        self.resetDirTip = Label(sWin, text="")
        self.resetDirTip.place(x=210,y=259,width=160)
        if self.darkMode:
            self.resetDirTip["bg"] = "#464646" # dark theme gray
            self.resetDirTip["fg"] = "#999999" # light theme gray
        else:
            self.resetDirTip['bg'] = "#ececec"
            self.resetDirTip["fg"] = "black"


        self.aprilFools = ttk.Label(sWin)
        self.aprilFools = Label(sWin, text="( ͡° ͜ʖ ͡°)", anchor=CENTER, wraplength=169, justify=CENTER)
        self.aprilFools["font"] = tkFont.Font(sWin, size=40)
        if self.darkMode:
            self.aprilFools["bg"] = "#464646" # dark theme gray
            self.aprilFools["fg"] = "#999999" # light theme gray
        else:
            self.aprilFools['bg'] = "#ececec"
            self.aprilFools["fg"] = "black"

        # print(datetime.now())
        if "-04-01" in str(datetime.now()):
            self.aprilFools.place(x=190,y=290,width=200)
        else:
            pass

        # Updates buttons when they are loaded initially. Scroll down to enbd of button script section to see
        self.updateButtons()


    # Scripting for buttons and other things
    def defaultDir_command(self):
        self.path = askdirectory()
        print(self.path)
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)

        with open(self.ymldir,"w+") as yml:
            data[0]['Options']['changedDefaultDir'] = True
            data[0]['Options']['defaultDir'] = self.path
            write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)


    def resetDefaultDir_command(self):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)

        with open(self.ymldir,"w+") as yml:
            data[0]['Options']['changedDefaultDir'] = False
            data[0]['Options']['defaultDir'] = self.dirDefaultSetting # done once reset
            write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
            self.resetDefaultDir["state"] = "disabled"
            self.resetDirTip["text"] = "Setting reset!"
        print("Reset the default directory in settings.")


    def togglePrefix(self): # Coudln't use the function for this, sticking with the value being a string for the sake of it
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)

        with open(self.ymldir,"w+") as yml:
            if self.prefixMenu['text'] == "Toggle On":
                self.filePrefix = ""
                self.prefixMenu["text"] = "Toggle Off"
                print("Prefix off!")
            else:
                self.filePrefix = "Scout_"
                self.prefixMenu["text"] = "Toggle On"
                print("Prefix on!")

            data[0]['Options']['hasFilePrefix'] = self.filePrefix
            write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)


    def toggleThumb(self):
        if self.thumbMenu['text'] == "Toggle On":
            self.thumbMenu["text"] = "Toggle Off"
        else:
            self.thumbMenu["text"] = "Toggle On"

        self.dump('thumbnail', self.thumbBool)


    def errorToggle(self):
        if self.warnMenu["text"] == "Toggle On":
            self.warnMenu["text"] = "Toggle Off"
        else:
            self.warnMenu["text"] = "Toggle On"
        self.dump('errorChoice', self.enablePrompts)


    def updateButtons(self):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            l = ["errorChoice", "hasFilePrefix", "thumbnail"]

            for i in data[0]['Options']:
                if i in l:
                    if i == 'errorChoice':
                        self.errorChoice = data[0]['Options'][str(i)]
                        if self.errorChoice:
                            self.warnMenu["text"] = "Toggle Off"
                        else:
                            self.warnMenu["text"] = "Toggle On"

                    elif i == 'hasFilePrefix':
                        self.filePrefix = data[0]['Options'][str(i)]
                        if self.filePrefix:
                            self.prefixMenu["text"] = "Toggle Off"
                        else:
                            self.prefixMenu["text"] = "Toggle On"

                    elif i == 'thumbnail':
                        self.thumbBool = data[0]['Options'][str(i)]
                        if self.thumbBool:
                            self.thumbMenu["text"] = "Toggle Off"
                        else:
                            self.thumbMenu["text"] = "Toggle On"

    # Dump function to write new values made by toggle buttons
    def dump(self, setting, var):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
#            print(str(data))

        with open(self.ymldir,"w+") as yml:
            data[0]['Options'][setting] = not data[0]['Options'][setting]
            write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
            var = data[0]['Options'][setting]
            print(var)
        print("\nCurrently updating settings.yml...")


# Docs for pytube
# https://python-pytube.readthedocs.io/en/latest/api.html

# ffmpeg simple guide
# https://opensource.com/article/17/6/ffmpeg-convert-media-file-formats
# https://docs.python.org/3/library/subprocess.html || subprocess docs


# Declaring root and looping it :D
if __name__ == "__main__":
    root = ThemedTk(themebg=True)
    app = App(root)
    root.mainloop()

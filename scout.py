import tkinter as tk
from tkinter import ttk
from tkinter import *
from pytube import YouTube
from pytube.exceptions import *
from tkinter.filedialog import *
from tkinter import messagebox
from ttkthemes import ThemedTk # dark mode theme and stuff
import tkinter.font as tkFont
import webbrowser
import getpass
from ruamel import yaml
import os
import wget
import distro
import platform
import time
import subprocess # used for ffmpeg (file formatting)
import shutil # mainly used for detecting ffmpeg installation
from datetime import datetime
from zipfile import ZipFile
import urllib.error
import ssl


#-*- coding: utf-8 -*-
# Above allows more charcters to mentioned IN THE CODE

class App:
    def __init__(self, parent):

        # Iniatiating variables for all sorts of stuff
        self.audioBool = False
        self.videoBool = False
        self.changedDefaultDir = bool
        self.dirDefaultSetting = ""
        self.fileLoc = ""
        self.thumbBool = bool
        self.videoRes = False
        self.hasFilePrefix = True
        self.filePrefix = ""
        self.path = ""
        self.darkMode = False
        self.maxModeUse = 0
        self.version = "v1.5"
        self.logFont = "No value!"
        self.getUser = getpass.getuser()
        self.OS = distro.name(pretty=False)
        self.ffmpegDir = self.fileLoc + "ffmpeg"
        self.videoq = "" # vid quality example: 720p
        self.audioq = "" # audio quality example: 128kbs
        self.videof = "" # vid format example: mp4
        self.audiof = "" # audio format example: wav


        ssl._create_default_https_context = ssl._create_unverified_context # fixed windows SSL cert issue

        ####################################################
        #                                                  #
        #             Backend Config and Logos             #
        #                                                  #
        ####################################################


        if "Windows" in platform.platform():
            self.OS = "Windows"
        else:
            pass



        # Sets various variables for each OS being used.
        # Fonts, directories, special boolean values, etc.
        if self.OS not in "Windows Darwin":
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
            self.ffmpegDir = "ffmpeg" # change this if you are downloading a seperate ffmpeg binary to config like macOS
            self.UIAttributes = { # dictionarys for each OS to match aesthics
                "Font": "Source Code Pro",
                "charSize": 10,
                "restartTextPos": 308,
                "logFont": "Courier",
                "logSize": 9,
                "verSize": 7
            }

        elif self.OS in "Darwin":
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
            self.ffmpegDir = "/Users/" + self.getUser + "/Library/Application\ Support/Scout/ffmpeg"
            self.UIAttributes = { # dictionarys for each OS to match aesthics
                "Font": "Source Code Pro",
                "charSize": 12,
                "restartTextPos": 302,
                "logFont": "Source Code Pro",
                "logSize": 10,
                "verSize": 12
            }

        elif self.OS in "Windows": # change value for new platform object
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
            self.ffmpegDir = self.fileLoc + "ffmpeg" # change this if you are downloading a seperate ffmpeg binary to config like macOS
            self.UIAttributes = { # pre-made attributes to be place holders for multiple tkinter parames later on
                "Font": "Courier",
                "charSize": 8,
                "restartTextPos": 302,
                "logFont": "Courier",
                "logSize": 8,
                "verSize": 8
            }



        ####################################################
        ### Updating and Restoring YML settings initally ###
        ####################################################

        # Summary of this block: This generates the YML from scratch if its outdated or doesnt exist, and ignores otherwise.
        # Uses sample yml "cache.yml" to compare it being the newest yml to a potentially old one. (Not enough or different settings).


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

        print(self.OS)

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
                yaml.dump(self.payload, f, Dumper=yaml.RoundTripDumper)
                print("if statement passes")
                f.close()
        # makes a copy of the newest yml/settings structure
        os.chdir(self.fileLoc)
        cache = open(self.cachedir, "w+")
        yaml.dump(self.payload, cache, Dumper=yaml.RoundTripDumper)
        cache.close()
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
                        print("s")
                        cache.close()
                        yaml.dump(self.payload, yml, Dumper=yaml.RoundTripDumper)
                        print("Cache updated!")


        # Organizing and downloading app icon for each OS #
        # Building scout on windows with Pyinstaller needs the .ico file for use at first!

        print("Attemping logo downloading...")
        url = "https://raw.githubusercontent.com/leifadev/scout/main/images/scout_logo.png"

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

        parent.title("Scout")
        parent.tk.call('wm', 'iconphoto', parent._w, self.icon)

        width=845
        height=350
        screenwidth = parent.winfo_screenwidth()
        screenheight = parent.winfo_screenheight()
        style = ttk.Style()

        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.darkMode = data[0]['Options']['darkMode']
            if self.darkMode:
                parent.set_theme("equilux")
            else:
                if self.OS in "Darwin":
                    parent['bg'] = "#ececec"
                    print("\nLaunching in light mode!")
                elif self.OS not in "Windows Darwin":
                    parent['bg'] = "#ececec"
                    print("\nLaunching in light mode!")


        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        parent.geometry(alignstr)
        parent.resizable(width=False, height=False)

        # DEPRECATED \/\/\/
        ## area where clicks are detected ##

#        frame = Frame(parent, width=100, height=30)
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
#        canvas.create_image(350,50,image=test)apply


        ## Menu items ##


        self.menubar = Menu(parent)
        self.filemenu = Menu(self.menubar, tearoff=0)

        try:
            self.filemenu.add_command(label="Cut", accelerator="Command+X", command=lambda: parent.focus_get().event_generate('<<Cut>>'))

            self.filemenu.add_command(label="Copy", accelerator="Command+C", command=lambda: parent.focus_get().event_generate('<<Copy>>'))

            self.filemenu.add_command(label="Paste", accelerator="Command+V", command=lambda: parent.focus_get().event_generate('<<Paste>>'))
            self.filemenu.add_command(label="Select All", accelerator="Command+A", command=lambda: parent.focus_get().select_range(0, 'END')) # Does not work as of now v1.5
        except KeyError as e:
            self.logfield.insert(END, f"ERROR: Paste and copying functions failed! Try again?")
            print(f"Paste and copying functions failed!\n{e}")

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", accelerator="Command+Q", command=lambda: parent.quit())
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)

        self.helpmenu.add_command(label="About", command=self.about_button)
        self.helpmenu.add_command(label="Help", command=self.helpButton_command)

        self.helpmenu.add_separator()

        self.helpmenu.add_command(label="Settings", command=self.settings_button)

        self.menubar.add_cascade(label="About", menu=self.helpmenu)

        self.menubar.entryconfig("About", state="normal")
        parent.config(menu=self.menubar)
        parent.update()   # Updates window at startup to be interactive and lifted, DO NOT TOUCH


        # self.menubar.entryconfig("Settings", state="disabled")

        ## Elements ##

        parent.lift() # lift window to the top

        self.urlfield = ttk.Entry(parent)
        self.urlfield["justify"] = "left"
        self.urlfield["text"] = ""
        self.urlfield.insert(0, '')   # add pre made message
        self.urlfield.place(x=20,y=60,width=540)


        self.downloadButton=ttk.Button(parent)
#        self.downloadButton["justify"] = "center"
        self.downloadButton["text"] = "Download"
        self.downloadButton.place(x=570,y=59,width=120)
        self.downloadButton["command"] = self.downloadButton_command


        self.browseButton=ttk.Button(parent)
        self.browseButton["text"] = "File Destination"
        self.browseButton["command"] = self.browseButton_command
        self.browseButton.place(x=690,y=59,width=140)


        self.videoButton=tk.Checkbutton(parent)
        self.videoButton["text"] = "Video"
        self.videoButton.place(x=730,y=130,width=70,height=30)
        self.videoButton["offvalue"] = False
        self.videoButton["onvalue"] = True
        self.videoButton["command"] = self.videoButton_command

        self.audioButton=tk.Checkbutton(parent)
        self.audioButton["text"] = "Audio"
        self.audioButton.place(x=730,y=190,width=70,height=30)
        self.audioButton["offvalue"] = False
        self.audioButton["onvalue"] = True
        self.audioButton["command"] = self.audioButton_command

        helpButton=ttk.Button(parent)
        helpButton["text"] = "Help"
        helpButton.place(x=20,y=300,width=70)
        helpButton["command"] = self.helpButton_command

        clearButton=ttk.Button(parent)
        clearButton["text"] = "Clear"
        clearButton.place(x=95, y=300,width=70)
        clearButton["command"] = self.clearConsole_command

        self.modeButton=ttk.Button(parent)
        self.modeButton.place(x=170,y=300,width=100)
        self.modeButton["command"] = self.switchMode


        self.versionText = tk.Label(parent)
        self.versionText = Label(parent, text=self.version)
        self.versionText.place(x=740,y=300,width=125,height=30)
        self.versionText["font"] = tkFont.Font(family=self.UIAttributes.get("Font"), size=self.UIAttributes.get("verSize"))



        ## All selections/menus for format and quailty choice ##

        self.clickedvf = StringVar()
        self.clickedvf.set("mp4")
        self.videoformat = ttk.OptionMenu(parent, self.clickedvf, "mp4", "mp4", "mov", "webm")
        self.videoformat["state"] = "normal"


        self.clickedaf = StringVar()
        self.clickedaf.set("mp4")
        self.audioformat = ttk.OptionMenu(parent, self.clickedaf, "mp3", "mp3", "wav", "ogg")
        self.audioformat["state"] = "normal"

        self.clickedvq = StringVar()
        self.clickedvq.set("Quality")
        self.videoquality = ttk.OptionMenu(parent, self.clickedvq, "Quality", "1080p", "720p", "480p", "360p", "240p", "144p")
        self.videoquality["state"] = "normal"

        self.clickedaq = StringVar()
        self.clickedaq.set("Quality")
        self.audioquality = ttk.OptionMenu(parent, self.clickedaq, "Quality", "160kbs", "128kbs", "70kbs", "50kbs")
        self.audioquality["state"] = "normal"


        # Block of code to switch bgs and fgs manually for darkMode using only tk not ttk
        # static values for checkbuttosn
        self.audioButton["highlightthickness"] = 0
        self.videoButton["highlightthickness"] = 0

        # dark/light mode dependent values, colors, formatting, etc.
        if self.darkMode:
            self.versionText["bg"] = "#464646" # dark theme gray
            self.versionText["fg"] = "#ececec" # light theme gray

            self.audioButton["bg"] = "#464646"
            self.videoButton["bg"] = "#464646"
            self.videoButton["activebackground"] = "#464646"
            self.videoButton["activeforeground"] = "#dadada"
            self.audioButton["activebackground"] = "#464646"
            self.audioButton["activeforeground"] = "#dadada"

            self.audioButton["fg"] = "#ececec"
            self.videoButton["fg"] = "#ececec"

            self.audioButton["selectcolor"] = "#a2a2a2"
            self.videoButton["selectcolor"] = "#a2a2a2"

        else:
            self.versionText['bg'] = "#ececec"
            self.versionText["fg"] = "#464646"

            self.audioButton["bg"] = "#ececec"
            self.videoButton["bg"] = "#ececec"



        # Loading dark mode value from settings.yml for inital launch
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.enablePrompts = data[0]['Options']['errorChoice']
            self.darkMode = data[0]['Options']['darkMode']
            if self.darkMode:
                self.modeButton["text"] = "Light Mode"
            else:
                self.modeButton["text"] = "Dark Mode"

        # Logfield #
        # Comes with error handling, video info, system/scout info/errors

        self.logfield = tk.Text(parent)
        self.logfield.place(x=20,y=100,width=540, height=180)
        ft = tkFont.Font(family=self.UIAttributes.get("logFont"), size=self.UIAttributes.get("logSize"))
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(END, "Scout launched successfully!\nVersion: " + self.version + "\n" + f'OS: {self.OS}\n')
        self.logfield["state"] = "disabled"
        if self.darkMode:
            self.logfield["bg"] = "#e5e5e5"
        else:
            self.logfield["bg"] = "#f6f6f6" # if you want change this into 1 line for a bg dont keep it there for future adjustments

    # Loading dark mode value from settings.yml for inital launch



    #############################################################################


    ## Triggers and Scripts ##
    # These coinside with the log field element itself

    # FFmpeg warning: For formatting one must install ffmpeg for video formatting

    def checkFFmpeg(self, quitBool):

        self.ffmpeg = bool

        if self.OS not in "Windows Darwin":
            if shutil.which('ffmpeg') is None:
                self.logfield["state"] = "normal"
                self.logfield.insert(END, f'\nWARNING: You do not have FFmpeg installed, and you cannot choose custom file types!\n |\n └ MacOS: Install homebrew and download it, "brew install ffmpeg". Install brew from \nhttps://brew.sh\n | \n └ Linux: Install it with your package manager, e.g. apt install ffmpeg.\n | \n └ Windows: Download through http://ffmpeg.org. Install here: https://github.com/leifadev/scout/wiki/Install-FFmpeg#windows.\n')
                self.ffmpeg = False
                self.logfield["state"] = "disabled"
                print("You don't have FFmpeg installed! You can't use custom file types.")
                # Disable menus that require ffmpeg
                self.audioquality["state"] = "disabled"
                self.videoquality["state"] = "disabled"
                self.videoformat["state"] = "disabled"
                self.audioformat["state"] = "disabled"
                print("\nFFmpeg isn't installed, read console for instructions!\n")
                print("Operating system is LINUX")
            else:
                self.ffmpeg = True
                print("\nYou have FFmpeg installed! You can use custom file types.\n")

        else:
            self.logfield["state"] = "normal"
            ext = "ffmpeg" if self.OS in "Darwin" else "ffmpeg.exe" # nice inline statement ;)
            if not os.path.isfile(self.fileLoc + ext):

                self.logfield["state"] = "normal"

                self.logfield.insert(END, f'\nINFO: WAIT! Please wait up to a minute (depending on your internet connection)\nfor scout to download video and audio conversion! This will only happen once.\n\n')

                self.logfield.insert(END, f'\nINFO: If you don\'t have an internet connection to install FFmpeg, wait until you do. Then relaunch scout when you have one.\nPlease go to the help button and to seek guidance on the wiki and more.')

                print("\nYou don\'t have FFmpeg installed! DONT WORRY, it will be installed automatically for you now!\n")

                print("\nDownloading latest stable version of ffmpeg, may take several seconds!\n")

                messagebox.showwarning("Warning", "You do not have FFmpeg library installed, please wait several seconds for it to install.\n\nInternet is required!")

                os.chdir(self.fileLoc)
                time.sleep(1)

                if self.OS in "Darwin":
                    wget.download("https://evermeet.cx/ffmpeg/getrelease/zip", self.fileLoc + "ffmpeg.zip")
                    with ZipFile("ffmpeg.zip", 'r') as zip: # extracts downloaded zip from ffmpegs download API for latest release
                        zip.extractall()
                        print("\nFile extracted...\n")

                elif self.OS in "Windows":
                    wget.download("https://github.com/leifadev/scout/blob/main/dependencies/ffmpeg.exe?raw=true")

                if self.OS in "Darwin": # run for perms for UNIX bs
                    try:
                        subprocess.run(f"chmod +x \"ffmpeg\"", shell=True) # gives perms for the file to be an executable like all binaries should be
                        print("\nFFmpeg binary is now executable! :)\n")
                    except:
                        print("Skipped macOS actions...")
                else:
                    pass

                try:
                    os.remove("ffmpeg.zip") # remove zipped file for clean dir and less space
                    print("\nPurged inital zip file\n")
                except:
                    print("Zip file not present, already deleted by the OS?")

                print("\nFFmpeg was sucessfully automatically installed to your config directory!\n")

                if quitBool:
                    messagebox.showinfo("Success!", "FFmpeg was installed! Restart.")
                    quit()
                else:
                    messagebox.showinfo("Success!", "FFmpeg was installed! Resuming download...")


            if os.path.isfile(self.fileLoc + "ffmpeg"): # chevck again if it is now installed
                print("\nFFmpeg is present in your config folder!\n(" + self.fileLoc + ")\n")
                self.ffmpeg = True
            elif os.path.isfile(self.fileLoc + "ffmpeg.exe"): # chevck again if it is now installed
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

        return self.checkFFmpeg

    ######################################################################################


    def videoFetch(self, yt, query): # Basic video basic report (used in all download types)
        self.yt = YouTube(query)
        self.query = self.urlfield.get()
        self.logfield.insert(END, f'\n---------------------------------------------------------------------')
        self.logfield.insert(END, f'\n\nStarting download to path: {self.path}')
        self.logfield.insert(END, f'\nVideo Title: {self.yt.title}')
        self.logfield.insert(END, f'\nVideo Author: {self.yt.author}')
        self.logfield.insert(END, f'\nPublish Date: {self.yt.publish_date}')
        self.logfield.insert(END, f'\nVideo Duration (sec): {self.yt.length}')
        self.logfield.insert(END, f'\nViews: {self.yt.views}')
        self.logfield.insert(END, f'\nRating ratio: {self.yt.rating}')
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

        # check if ffmpeg binary is present if not for whatever reason...?
        self.checkFFmpeg(False)

        try:
            self.logfield["state"] = "normal"

            self.query = self.urlfield.get() # gets entry input
            self.yt = YouTube(self.query)

        except RegexMatchError as e:
            print("Regex match error! Invalid...\n" + str(e) + "\n")
            self.logfield["state"] = "normal" # disable log after any erros are detected
            self.logfield.insert(END, f'\nERROR: Regex could not parse URL field!\n')
            self.logfield["state"] = "disabled" # disable log after any erros are detected

        except urllib.error.HTTPError as err:
            print("\n\nThere was a (maybe) 404 Not Found error!\n" + str(err) + "\n")
            self.logfield["state"] = "normal" # disable log after any erros are detected
            self.logfield.insert(END, f'\nERROR: There was a 404 Not Found error. Internet down?\nOtherwise may be a (temporary) bug on the backend.\n\nBring this to the github.\n')
            self.logfield["state"] = "disabled" # disable log after any erros are detected

        # Thumbnail download
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.thumbBool = data[0]['Options']['thumbnail']
            if self.thumbBool:
                wget.download(self.yt.thumbnail_url, self.path + "/" + self.filePrefix + self.yt.title + ".jpg")
                print("\nDownloading the thumbnail as well :) \nIf your seeing this and your thumbnail setting is off, please delete your config file and restart scout.\nConfig file path: " + self.ymldir + "\n")


        if self.videoBool and self.audioBool: # Video and Audio
            self.logfield["state"] = "normal"
            try:
                self.query = self.urlfield.get()
                self.yt = YouTube(self.query)
                res = self.clickedvq.get()
                # This block searches through a dictionary of known quality values, then suggests available values later
                streams = str(self.yt.streams.filter(progressive=True).all())
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
                except Exception as e:
                    print("\nNo other available values were found to fallback on, check for any stream query objects above!\n" + str(e))

                videoDown = self.yt.streams.filter(res=res, progressive=True).first()
                print(res)
                print(f'\nAvailable stream(s):\n{videoDown}', f'All streams:\n{streams}')

                # Block that converts custom file types, video/audio #

                if videoDown is None: # This tiny block for error handling no known download settings, suggests them afterwards
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

                    filtered = self.yt.title.translate({ord(i): None for i in '=|;:/"\',.?*^%$#'}) # filter fetched yt title and remove all special chars, as pytube removes them when it downloads the first one we need to mod

                    subprocess.run(f"chmod 755 \"{filtered}.mp4\"", shell=True) # give perms for file with ffmpeg
                    self.logfield.insert(END, f'\nINFO: Converting inital file to .{self.clickedvf.get()}\n')

                    # Running ffmpeg in console with subprocess, multiple flags to leave out extra verbose output from ffpmeg, and say yes to all arguments
                    subprocess.run(f'{self.ffmpegDir} -hide_banner -loglevel error -y -i \"{self.fileLoc}{filtered}.mp4\" \"{self.path}{self.path_slash}{filtered}.{self.clickedvf.get()}\"', shell=True)

                    self.logfield.insert(END, f'\nINFO: Removing temp file...\n')
                    os.remove(f"{filtered}.mp4")

                    print("Original file deleted! Enjoy your converted one")

                    self.logfield.insert(END, f'\nINFO: The {videoDown}, codec/itag was used.\n') # This and below show in the log what actually stream object they downloaded with there video. Helpful for debugging!
                    self.videoFetch(self.yt, self.query) # Fetching post-log video info, function up top this download function
                else:
                    print(f'\n\n{self.path}\n\n')
                    videoDown.download(self.path, filename_prefix=self.filePrefix)
                    self.logfield.insert(END, f'\nINFO: The {videoDown}, codec/itag was used.\n')
                    self.videoFetch(self.yt, self.query)

                self.videoFetch(self.yt, self.query)
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
                self.query = self.urlfield.get()
                self.yt = YouTube(self.query)
                audioDown = self.yt.streams.filter(abr=self.audioq, only_audio=True).first()
                abr = self.clickedaq.get()
                streams = str(self.yt.streams.filter(only_audio=True).all())
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
                except Exception as e:
                    print("\nNo other available values were found to fallback on, check for any stream query objects above!\n" + str(e))

                print(abr)
                print(f'\nAvailable stream(s):\n{audioDown}', f'All streams:\n{streams}')

                if audioDown is None: # This tiny block for error handling no known download settings, suggests them afterwards
                    self.logfield.insert(END, f'\nERROR: This video is unavailable with these download settings!\n')

                    print("Gathered available quality options: ", aAbr) # extra verbose input
                    suggestMsg = f'\nINFO: Try the {aAbr} resolutions instead\n'
                    self.logfield.insert(END, f'{suggestMsg}')

                    self.logfield["state"] = "disabled"
                    return

                audioDown.download(self.fileLoc, filename_prefix=self.filePrefix)
                os.chdir(self.fileLoc)
                print("\n\n"+os.getcwd()+"\n\n")
                self.logfield.insert(END, f'\n---------------------------------------------------------------------\nINFO: Modding file permissions...\n')
                filtered = self.yt.title.translate({ord(i): None for i in '=|;:/,.?*^%$#\'"'})
                subprocess.run(f"chmod 755 \"{filtered}.mp4\"", shell=True) # give perms for file with ffmpeg
                self.logfield.insert(END, f'\nINFO: Converting inital file to .{self.clickedaf.get()}\n')
                subprocess.run(f'{self.ffmpegDir} -hide_banner -loglevel error -y -i \"{self.fileLoc}{filtered}.mp4\" \"{self.path}{self.path_slash}{filtered}.{self.clickedaf.get()}\"', shell=True)
                self.logfield.insert(END, f'\nINFO: Removing temp file...\n')
                os.remove(f"{filtered}.mp4")

                print("Original file deleted! Enjoy your converted one")

                self.logfield.insert(END, f'\nINFO: The {audioDown}, codec/itag was used.\n')

                self.videoFetch(self.yt, self.query)
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
                # self.logfield.insert(END, f'\nINFO: These downloads take extra long, don\'t quit me!\n')
            try:
                self.yt = YouTube(self.query)
                silent_audioDown = self.yt.streams.filter(res=self.videoq, only_video=True).first()
                res = self.clickedvq.get()
                streams = str(self.yt.streams.filter(only_video=True).all())
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

                except Exception as e:
                    print("\nNo other available values were found to fallback on, check for any stream query objects above!\n" + str(e))

                print(res)
                print(f'\nAvailable stream(s):\n{silent_audioDown}', f'All streams:\n{streams}')

                if silent_audioDown is None: # This tiny block for error handling no known download settings, suggests them afterwards
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
                    filtered = self.yt.title.translate({ord(i): None for i in '=|;:/,.?*^%$#\'"'})
                    subprocess.run(f"chmod 755 \"{filtered}.mp4\"", shell=True) # give perms for file with ffmpeg
                    self.logfield.insert(END, f'\nINFO: Converting inital file to .{self.clickedvf.get()}\n')
                    subprocess.run(f'{self.ffmpegDir} -hide_banner -loglevel error -y -i \"{self.fileLoc}{filtered}.mp4\" \"{self.path}{self.path_slash}{filtered}.{self.clickedvf.get()}\"', shell=True)
                    self.logfield.insert(END, f'\nINFO: Removing temp file...\n')
                    os.remove(f"{filtered}.mp4")

                    print("Original file deleted! Enjoy your converted one")

                    self.logfield.insert(END, f'\nINFO: The {silent_audioDown}, codec/itag was used.\n')
                else:
                    silent_audioDown.download(self.path, filename_prefix=self.filePrefix)
                    self.logfield.insert(END, f'\nINFO: The {silent_audioDown}, codec/itag was used.\n')

                self.videoFetch(self.yt, self.query)
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

            self.query = self.urlfield.get() # gets entry input (the users specifed URL)

            if self.urlfield.get() == "":
                self.logfield["state"] = "normal" # disable log after any erros are detected

            elif self.enablePrompts: # hasnt selected video nor audio
                self.logfield.insert(END, f'\nERROR: You can\'t download a video without video or audio!\n')

            self.logfield["state"] = "disabled" # disabled the entirity again


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

        self.dump('darkMode', self.darkMode)

        # Stop more than 1 use for user to restart app, avoid spam clicking issues and such
        self.maxModeUse += 1
        if self.maxModeUse == 1:
            self.modeButton["state"] = "disabled"
            self.maxWarn = Label(parent, text=self.version)
            if self.darkMode == False:
                self.maxWarn["fg"] = "#464646" # light theme gray
                self.maxWarn["bg"] = "#ececec"
            else:
                self.maxWarn["fg"] = "#ececec" # If statement checking if darkMode is on and to switch bg accordingly
                self.maxWarn["bg"] = "#464646"
            self.maxWarn.place(x=280,y=302,width=140)
            self.maxWarn["text"] = "Restart to apply!"
            self.menubar.entryconfig("About", state="disabled")
            self.maxWarn["font"] = tkFont.Font(family=self.UIAttributes.get("Font"), size=self.UIAttributes.get("charSize"))

    # This is function for the "File Destination" button in the main menu
    # Uses tkinter and fetches yml values to work
    def browseButton_command(self):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.path = data[0]['Options']['defaultDir'] # Fetch any set default directories specificed in settings pane
            self.changedDefaultDir = data[0]['Options']['changedDefaultDir']

        # First we load the data of the defaultDir value, regardless if we need it for the a selected default directory in settings by the user
        if self.changedDefaultDir:
            askdirectory(initialdir=self.path) # If the default directory feature was used with a custom path, we will use it from the YML settings file
        else:
            print("* Not using a default custom directory!")
            self.path = askdirectory(initialdir=self.path) # Else if the boolean was false, we simply override the fetched self.path with the default desktop directory!
            self.path = self.dirDefaultSetting
        print(self.path)

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
        webbrowser.open("https://github.com/leifadev/scout/wiki#help")
        self.logfield["state"] = "normal"
        self.logfield.insert(END, "\n\nINFO: Launched help page! Documentation, Code, Wiki, and more :)\n")
        self.logfield["state"] = "disabled"
        print("This is opening the github page to for Scout. All versions of scout, a public wiki, and an issues page\nare there to help!")

    # Clear the whole test entry, deleting line until the end, still restarting the welcome message!
    def clearConsole_command(self):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.enablePrompts = data[0]['Options']['errorChoice'] # Fetch any set default directories specificed in settings pane
        self.logfield["state"] = "normal"
        if self.enablePrompts:
            messagebox.showwarning("Warning", "Are you sure you want to clear the console?")
            self.logfield.delete("1.0","end")
            self.logfield.insert(END, "Scout launched successfully!\nVersion: " + self.version + "\n" + f'OS: {self.OS}\n')
        else:
            self.logfield.delete("1.0","end")
            self.logfield.insert(END, "Scout launched successfully!\nVersion: " + self.version + "\n" + f'OS: {self.OS}\n')
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
        abtMsg = "Author: leifadev\nLicense: GPL/GNU v3\nVersion: " + self.version + "\n\nLanguage: Python 3.6+\nCompilier: Pyinstaller\nFramework: Tkinter"
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
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.enablePrompts = data[0]['Options']['errorChoice']
            self.darkMode = data[0]['Options']['darkMode']
            self.filePrefix = data[0]['Options']['hasFilePrefix']
            self.thumbBool = data[0]['Options']['thumbnail']

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
        self.resetDefaultDir.place(x=200,y=225,width=180)
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
        print(f'\nSelected path: {self.path}')
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            with open(self.ymldir, "w+") as yml:
                self.changedDefaultDir = True
                data[0]['Options']['changedDefaultDir'] = self.changedDefaultDir
                data[0]['Options']['defaultDir'] = self.path
                write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)


    def resetDefaultDir_command(self):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            with open(self.ymldir, "w+") as yml:
                self.changedDefaultDir = False
                data[0]['Options']['changedDefaultDir'] = self.changedDefaultDir
                data[0]['Options']['defaultDir'] = self.dirDefaultSetting # done once reset
                write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
                self.resetDefaultDir["state"] = "disabled"
                self.resetDirTip["text"] = "Setting reset!"
        print("Reset the default directory in settings.")


    def togglePrefix(self): # Coudln't use the function for this, sticking with the value being a string for the sake of it
        if self.prefixMenu['text'] == "Toggle On":
            self.filePrefix = ""
            self.prefixMenu["text"] = "Toggle Off"
            print("Prefix off!")
        else:
            self.filePrefix = "Scout_"
            self.prefixMenu["text"] = "Toggle On"
            print("Prefix on!")
        self.dump('hasFilePrefix', self.filePrefix)


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
            self.enablePrompts = data[0]['Options']['errorChoice']
            self.filePrefix = data[0]['Options']['hasFilePrefix']
            self.thumbBool = data[0]['Options']['thumbnail']
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


    # Dump function to write new values made by toggle buttons, etc.
    def dump(self, setting, var):
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            # print(f'\nHERE IT IS\n{data}\n')
            self.enablePrompts = data[0]['Options']['errorChoice']
            self.darkMode = data[0]['Options']['darkMode']
            self.filePrefix = data[0]['Options']['hasFilePrefix']
            self.thumbBool = data[0]['Options']['thumbnail']
            self.changedDefaultDir = False

            with open(self.ymldir,"w+") as yml:
                data[0]['Options'][setting] = not data[0]['Options'][setting]
                write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
                var = data[0]['Options'][setting]
                print(var, setting)
        print("\nCurrently updating settings.yml...")


# Docs for pytube
# https://python-pytube.readthedocs.io/en/latest/api.html

# ffmpeg simple guide
# https://opensource.com/article/17/6/ffmpeg-convert-media-file-formats
# https://docs.python.org/3/library/subprocess.html || subprocess docs

# docs: https://github.com/leifadev/scout/wiki

# def quitall():
#     print("QUITTING ALL WINDOWS")
#     parent.quit()
#     sWin.quit()

# Declaring parent and looping it :D
if __name__ == "__main__":
    parent = ThemedTk(themebg=True)
    app = App(parent)
    # parent.protocol("WM_DELETE_WINDOW", quitall())
    parent.mainloop()

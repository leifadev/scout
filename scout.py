import tkinter as tk # main gui framework
from tkinter import *
import webbrowser
from tkinter.filedialog import askdirectory
from pytube import YouTube
import getpass
from tkinter import messagebox
from ruamel import yaml
import os
import tkinter.font as tkFont
from pytube.exceptions import * # all excpetions I use for error handling in log field
import wget
import ssl
from sys import platform as _platform
from tkinter import ttk
from ttkthemes import ThemedTk,THEMES # dark mode theme and stuff
from PIL import Image, ImageTk
import filecmp
import subprocess # used for ffmpeg (file formatting)
import shutil # used for detecting ffmpeg installation, could be use for more after this comment is made


class App:
    def __init__(self, root):

        # Iniatiating variables, some temporary, some stored in settings.yml
        self.audioBool = False
        self.videoBool = False
        self.changedDefaultDir = bool
        self.videoRes = False
        self.filePrefix = ""
        ssl._create_default_https_context = ssl._create_unverified_context
        self.path = ""
        self.darkMode = False
        self.maxModeUse = 0
        self.version = "v1.4"
        self.logFont = "No value!"
        self.getUser = getpass.getuser()
        self.videoq = "" # vid quality example: 720p
        self.audioq = "" # audio quality example: 128kbps
        self.videof = "" # vid format example: mp4
        self.audiof = "" # audio format example: wav
        # DEVS DONT INCLUDE "."s ^^^BEFORE EXTENSIONS^^^


        ####################################################
        #                                                  #
        #             Backend Config and Logos             #
        #                                                  #
        ####################################################

        # check OS
        if _platform in ("linux", "linux2"):
            self.fileLoc = "/home/" + self.getUser + "/Documents/Scout/"
            dirDefaultSetting = "/Users/" + self.getUser + "/Desktop"
            self.ymldir = "/home/" + self.getUser + "/Documents/Scout/settings.yml"
            self.cachedir = "/home/" + self.getUser + "/Documents/Scout/cache.yml"
            if self.path ==  "":
                self.path = "/home/" + self.getUser + "/Desktop"
            else:
                print("You don't have a selected path! Defaulting your desktop.\nFor more help use the help button to our github.")
            self.logFont = 'Courier' # font that fits the OS UI
            self.logSize = "12"
            self.restartMsgY = None
            self.UIAttributes = { # dictionarys for each OS to match aesthics
                "Font": "Source Code Pro",
                "charSize": 10,
                "restartTextPos": 308,
                "logFont": "Courier",
                "logSize": 8
            }

        elif _platform == "darwin":
            self.fileLoc = "/Users/" + self.getUser + "/Library/Application Support/Scout/"
            dirDefaultSetting = "/Users/" + self.getUser + "/Desktop"
            self.cachedir = "/Users/" + self.getUser + "/Library/Application Support/Scout/cache.yml"
            self.ymldir = "/Users/" + self.getUser + "/Library/Application Support/Scout/settings.yml"
            if self.path ==  "":
                self.path = "/Users/" + self.getUser + "/Desktop"
            else:
                print("You don't have a selected path! Defaulting your desktop.\nFor more help use the help button to our github.")
            self.logFont = 'Source Code Pro'
            self.logSize = "12"
            self.restartMsgY = None
            self.UIAttributes = { # dictionarys for each OS to match aesthics
                "Font": "Source Code Pro",
                "charSize": 10,
                "restartTextPos": 302,
                "logFont": "Source Code Pro",
                "logSize": 8
            }

        elif _platform in ("win64", "win32"):
            self.fileLoc = "C:\\Users\\" + self.getUser + "\\Appdata\\Roaming\\Scout\\"
            dirDefaultSetting = "C:\\Users\\" + self.getUser + "\Desktop"
            self.ymldir = "C:\\Users\\" + self.getUser + "\\AppData\\Roaming\\Scout\\settings.yml"
            self.cachedir = "C:\\Users\\" + self.getUser + "\\AppData\\Roaming\\Scout\\cache.yml"
            if self.path ==  "":
                self.path = "C:\\Users\\" + self.getUser + "\Desktop"
            else:
                print("You don't have a selected path! Defaulting your desktop.\nFor more help use the help button to our github.")
            self.logFont = 'Courier'
            self.logSize = "9"
            self.restartMsgY = None
            self.UIAttributes = { # pre-made attrbutes to be place holders for multiple tkinter parames later on
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
                    'defaultDir': dirDefaultSetting,
                    'errorChoice': True,
                    'changedDefaultDir': False,
                    'hasFilePrefix': self.filePrefix,
                    'darkMode': self.darkMode
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
                    print("Launching in light mode!")
                elif _platform == "linux" or _platform == "linux2":
                    root['bg'] = "#ececec"
                    print("Launching in light mode!")


        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)


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


        # Menu items #

        menubar = Menu(root)
        filemenu = Menu(menubar)
        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="Cut", accelerator="Command+X", command=lambda: root.focus_get().event_generate('<<Cut>>'))

        filemenu.add_command(label="Copy", accelerator="Command+C", command=lambda: root.focus_get().event_generate('<<Copy>>'))

        filemenu.add_command(label="Paste", accelerator="Command+V", command=lambda: root.focus_get().event_generate('<<Paste>>'))
        filemenu.add_command(label="Select All", accelerator="Command+A", command=lambda: root.focus_get().select_range(0, 'end'))

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=root.quit)
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
        self.videoButton.place(x=720,y=120,width=70,height=30)
        self.videoButton["offvalue"] = False
        self.videoButton["onvalue"] = True
        self.videoButton["command"] = self.videoButton_command

        self.audioButton=tk.Checkbutton(root)
        self.audioButton["text"] = "Audio"
        self.audioButton.place(x=720,y=170,width=70,height=30)
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
        self.versionText["font"] = tkFont.Font(family='Courier', size=12)
        if self.darkMode:
            self.versionText["bg"] = "#464646" # dark theme gray
            self.versionText["fg"] = "#ececec" # light theme gray
        else:
            self.versionText['bg'] = "#ececec"
            self.versionText["fg"] = "#464646"

            #background color for Checkbuttons
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

        self.logfield = tk.Text(root)
        self.logfield.place(x=20,y=100,width=540, height=180)
        ft = tkFont.Font(family="Courier", size=10)
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(INSERT, "Scout launched successfully!\nVersion: " + self.version + "\n")
        self.logfield["state"] = "disabled"
        if self.darkMode:
            self.logfield["bg"] = "#e5e5e5"
        else:
            self.logfield["bg"] = "#f6f6f6" # if you want change this into 1 line for a bg dont keep it there for future adjustments


    ######################################################################################

    ## Triggers and Scripts ##
    # These coinside with the log field element itself

    # FFmpeg warning: For formatting one must install ffmpeg for video formatting

        self.ffmpeg = bool
        
        if shutil.which('ffmpeg') == None:
            # messagebox.showwarning("Warning", "Video resolutions for this option are lower quailty.")
            self.logfield["state"] = "normal"
            self.logfield.insert(INSERT, f'\nWARNING: You do not have FFmpeg installed, and you cannot choose custom file types!\n |\n | MacOS: Install homebrew and download it, "brew install ffmpeg". Install brew from \nhttps://brew.sh\n | \n | Linux: Install it with your package manager, e.g. apt install ffmpeg.\n | \n | Windows: Install it through http://ffmpeg.org. If it is installed, make sure that the folder of the ffmpeg executable is on the PATH.\n')
            self.ffmpeg = False
            self.logfield["state"] = "disabled"
            print("You don't have FFmpeg installed! You can't use custom file types.")
        else:
            self.ffmpeg = True
            print("You have FFmpeg installed! You can use custom file types.")

    ######################################################################################


    def videoFetch(self, yt, query): # Basic video basic report (used in all download types)
        yt = YouTube(query)
        query = self.urlfield.get()
        self.logfield.insert(INSERT, f'\n\nStarting download to path: {self.path}')
        self.logfield.insert(INSERT, f'\nVideo Title: {yt.title}')
        self.logfield.insert(INSERT, f'\nVideo Author: {yt.author}')
        self.logfield.insert(INSERT, f'\nPublish Date: {yt.publish_date}')
        self.logfield.insert(INSERT, f'\nVideo Duration (sec): {yt.length}')
        self.logfield.insert(INSERT, f'\nViews: {yt.views}')
        self.logfield.insert(INSERT, f'\nRating ratio: {yt.rating}')
        self.logfield.insert(INSERT, f'\n\n---------------------------------------------------------------------\n\n')

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

    # ffmpeg -hide_banner -loglevel error -y -i xbox.mp3 xboxx.wav

    # Download buttons scripting, includes all features said abive

    def downloadButton_command(self):
        self.videoq = ""
        self.audioq = ""
        self.videof = ""
        self.audiof = ""
        self.vfps = 30
        self.mime_type = ""

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
            self.logfield["state"] = "normal"

            query = self.urlfield.get() # gets entry input
            yt = YouTube(query)

        except RegexMatchError:
            self.logfield["state"] = "disabled"


        if self.videoBool and self.audioBool: # Video and Audio
            self.logfield["state"] = "normal"
            try:
                yt = YouTube(query)
                print("Okie dokie!")
                videoDown = yt.streams.filter(mime_type="video/" + self.videof, fps=self.vfps, res=self.videoq, abr=self.audioq, progressive=True).first()
                try:
                    videoDown.download(self.path, filename_prefix=self.filePrefix)
                    print(yt.streams.filter(res="720p", progressive=True).all())
                except:
                    self.logfield.insert(INSERT, f'\nERROR: This video is unavailable with these download settings\n')
                self.logfield.insert(INSERT, f'{videoDown}')
                self.videoFetch(yt, query)

            # Try statments using pytube errors repeats for each selection mode of video
            except VideoPrivate:
                self.logfield.insert(INSERT, error_dict.get('VideoPrivate'))
            except RegexMatchError:
                self.logfield.insert(INSERT, error_dict.get('RegexMatchError'))
            except RecordingUnavailable:
                self.logfield.insert(INSERT, error_dict.get('RecordingUnavailable'))
            except MembersOnly:
                self.logfield.insert(INSERT, error_dict.get('MembersOnly'))
            except LiveStreamError:
                self.logfield.insert(INSERT, error_dict.get('LiveStreamError'))
            except HTMLParseError:
                self.logfield.insert(INSERT, error_dict.get('HTMLParseError'))
            except VideoUnavailable:
                 self.logfield.insert(INSERT, error_dict.get('VideoUnavailable'))
            self.logfield["state"] = "disabled"


        elif self.audioBool:  # Audio only
            self.logfield["state"] = "normal"
            try:
                yt = YouTube(query)
                query = self.urlfield.get()
                try:
                    audioDown = yt.streams.filter(abr=self.audioq, only_audio=True).first()
                    high_audioDown.download(self.path, filename_prefix=self.filePrefix)
                # print(yt.streams.filter(only_audio=True).all())
                except:
                    self.logfield.insert(INSERT, f'\nERROR: This video is unavailable with these download settings\n')

                self.logfield.insert(INSERT, f'{audioDown}')
                self.videoFetch(yt, query)

            # Try statments using pytube errors repeats for each selection mode of video
            except VideoPrivate:
                self.logfield.insert(INSERT, error_dict.get('VideoPrivate'))
            except RegexMatchError:
                self.logfield.insert(INSERT, error_dict.get('RegexMatchError'))
            except RecordingUnavailable:
                self.logfield.insert(INSERT, error_dict.get('RecordingUnavailable'))
            except MembersOnly:
                self.logfield.insert(INSERT, error_dict.get('MembersOnly'))
            except LiveStreamError:
                self.logfield.insert(INSERT, error_dict.get('LiveStreamError'))
            except HTMLParseError:
                self.logfield.insert(INSERT, error_dict.get('HTMLParseError'))
            except VideoUnavailable:
                 self.logfield.insert(INSERT, error_dict.get('VideoUnavailable'))
            self.logfield["state"] = "disable"

        elif self.audioBool == False and self.videoBool: # Video only
            self.logfield["state"] = "normal"
            if self.enablePrompts:
                messagebox.showwarning("Warning", "Video resolutions for this option are lower quailty.")
                self.logfield.insert(INSERT, f'\nINFO: As of now videos downloaded without audio are fixed to 360p\n')
            try:
                yt = YouTube(query)
                query = self.urlfield.get()
                try:
                    silent_audioDown = yt.streams.filter(mime_type="video/" + self.videof, fps=self.vfps, res=self.videoq)
                    silent_audioDown.download(self.path, filename_prefix=self.filePrefix)
                except:
                    self.logfield.insert(INSERT, f'\nERROR: This video is unavailable with these download settings\n')

                self.logfield.insert(INSERT, f'{silent_audioDown}')
                self.videoFetch(yt, query)

            # Try statments using pytube errors repeats for each selection mode of video
            except VideoPrivate:
                self.logfield.insert(INSERT, error_dict.get('VideoPrivate'))
            except RegexMatchError:
                self.logfield.insert(INSERT, error_dict.get('RegexMatchError'))
            except RecordingUnavailable:
                self.logfield.insert(INSERT, error_dict.get('RecordingUnavailable'))
            except MembersOnly:
                self.logfield.insert(INSERT, error_dict.get('MembersOnly'))
            except LiveStreamError:
                self.logfield.insert(INSERT, error_dict.get('LiveStreamError'))
            except HTMLParseError:
                self.logfield.insert(INSERT, error_dict.get('HTMLParseError'))
            except VideoUnavailable:
                 self.logfield.insert(INSERT, error_dict.get('VideoUnavailable'))
            self.logfield["state"] = "disabled"
        else:
            self.logfield["state"] = "normal" # disable log after any erros are detected

            query = self.urlfield.get() # gets entry input (the users specifed URL)

            if self.urlfield.get() == "":
                self.logfield.insert(INSERT, f'\nERROR: URL field is empty and cannot be parsed')

            elif self.enablePrompts: # hasnt selected video nor audio
                self.logfield.insert(INSERT, f'\nERROR: You can\'t download a video with video or audio\n')

            self.logfield["state"] = "disabled" # disabled the entirity again

    def formatFile(self, audiof, videof):
        print("Test")


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
                self.maxWarn["fg"] = "#ececec"
                self.maxWarn["bg"] = "#464646"
            self.maxWarn.place(x=280,y=302,width=140)
            self.maxWarn["text"] = "Restart to apply!"
            self.maxWarn["font"] = tkFont.Font(family="Source Code Pro", size=12)


    def browseButton_command(self):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.path = data[0]['Options']['defaultDir']

        if self.changedDefaultDir:
            askdirectory(initialdir=self.path)
        else:
            askdirectory(initialdir='/Users/' + self.getUser + '/Desktop/')


    def videoButton_command(self):
        if self.videoBool == False:
            self.videoBool = True
        else:
            self.videoBool = False
        print("Video status: " + str(self.videoBool))


    def audioButton_command(self):
        if self.audioBool == False:
            self.audioBool = True
        else:
            self.audioBool = False
        print("Audio status: " + str(self.audioBool))

    def helpButton_command(self):
        webbrowser.open("https://github.com/leifadev/scout")
        print("This is opening the github page to for Scout. All versions of scout, a public wiki, and an issues page\nare there to help!")

    # Clear the whole test entry, deleting line until the end, still restarting the welcome message!
    def clearConsole_command(self):
        self.logfield["state"] = "normal"
        if self.enablePrompts:
            messagebox.showwarning("Warning", "Are you sure you want to clear the console?")
            self.logfield.delete("1.0","end")
            self.logfield.insert(INSERT, "Scout launched successfully!\nVersion: " + self.version + "\n")
        else:
            self.logfield.delete("1.0","end")
            self.logfield.insert(INSERT, "Scout launched successfully!\nVersion: " + self.version + "\n")
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

        self.abtTitle = ttk.Label(abt)
        self.abtTitle = Label(abt, text="About")
        self.abtTitle.place(x=45,y=10,width=210)
        if self.darkMode:
            self.abtTitle["bg"] = "#464646" # dark theme gray
            self.abtTitle["fg"] = "#999999" # light theme gray
        else:
            self.abtTitle['bg'] = "#ececec"
            self.abtTitle["fg"] = "black"

        abtMsg = "Author: leifadev\nLicense: GPL/GNU v3\nVersion: " + self.version + "\n\nLanguage: Python 3\nCompilier: Pyinstaller\nFramework: Tkinter"
        self.msg = ttk.Label(abt)
        self.msg = Label(abt, text=abtMsg, anchor=CENTER, wraplength=160, justify=CENTER)
        self.msg.place(x=50,y=40,width=200)
        if self.darkMode:
            self.msg["bg"] = "#464646" # dark theme gray
            self.msg["fg"] = "#999999" # light theme gray
        else:
            self.msg['bg'] = "#ececec"
            self.msg["fg"] = "black"


        self.abtLink = "Contribute to the wiki!"
        self.abtLink = ttk.Label(abt)
        self.abtLink = Label(abt, font= ('Courier 12 underline'), text="Contribute to the wiki!", anchor=CENTER, wraplength=160, justify=CENTER)
        self.abtLink.place(x=50,y=170,width=200)
        self.abtLink["fg"] = "#2f81ed"
        self.abtLink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/leifadev/scout/wiki"))
        if self.darkMode:
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
            self.settingsTitle['bg'] = "#ececec"
            self.settingsTitle["fg"] = "black"

        self.defaultDirButton=ttk.Button(sWin, text="Choose") # Disabled default dir until further notice
#        self.defaultDirButton["text"] = "Choose"
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
        self.warnMenu.place(x=292,y=102,width=110)
        self.warnMenu["command"] = self.errorToggle     #  toggle button for prompts lolz

        self.warnTip = ttk.Label(sWin)
        self.warnTip = Label(sWin, text="Recieve Prompts")
        self.warnTip.place(x=165,y=108,width=110)
        if self.darkMode:
            self.warnTip["bg"] = "#464646" # dark theme gray
            self.warnTip["fg"] = "#999999" # light theme gray
        else:
            self.warnTip['bg'] = "#ececec"
            self.warnTip["fg"] = "black"

        self.prefixMenu = ttk.Button(sWin)
        self.prefixMenu["text"] = "Toggle Off"
        self.prefixMenu.place(x=292,y=152,width=110)
        self.prefixMenu["command"] = self.togglePrefix   # SECOND

        self.prefixTip = ttk.Label(sWin)
        self.prefixTip = Label(sWin, text="File Prefix")
        self.prefixTip.place(x=165,y=157,width=110)
        if self.darkMode:
            self.prefixTip["bg"] = "#464646" # dark theme gray
            self.prefixTip["fg"] = "#999999" # light theme gray
        else:
            self.prefixTip['bg'] = "#ececec"
            self.prefixTip["fg"] = "black"

        self.resetDefaultDir = ttk.Button(sWin)
        self.resetDefaultDir["text"] = "Reset Default Directory"
        self.resetDefaultDir.place(x=210,y=201,width=170)
        self.resetDefaultDir["command"] = self.resetDefaultDir_command
        self.resetDefaultDir["state"] = "normal"

        self.resetDirTip = ttk.Label(sWin)
        self.resetDirTip = Label(sWin, text="")
        self.resetDirTip.place(x=210,y=235,width=160)
        if self.darkMode:
            self.resetDirTip["bg"] = "#464646" # dark theme gray
            self.resetDirTip["fg"] = "#999999" # light theme gray
        else:
            self.resetDirTip['bg'] = "#ececec"
            self.resetDirTip["fg"] = "black"

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
            data[0]['Options']['defaultDir'] = None # done once reset
            write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
            self.resetDefaultDir["state"] = "disabled"
            self.resetDirTip["text"] = "Setting reset!"
        print("Reset the default directory in settings.")


    def togglePrefix(self):
        if self.filePrefix == "Scout_":
            self.filePrefix = ""
            self.prefixMenu["text"] = "Toggle Off"
            print("Prefix off!")
        else:
            self.filePrefix = "Scout_"
            self.prefixMenu["text"] = "Toggle On"
            print("Prefix on!")

        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)

        with open(self.ymldir,"w+") as yml:
            data[0]['Options']['hasFilePrefix'] = self.filePrefix
            write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
            self.filePrefix = data[0]['Options']['hasFilePrefix']
            print(self.filePrefix)
        print("\nCurrently updating settings.yml...")


    def errorToggle(self):
        if self.warnMenu["text"] == "Toggle On":
            self.warnMenu["text"] = "Toggle Off"
        else:
            self.warnMenu["text"] = "Toggle On"
        self.dump()


    def dump(self):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
#            print(str(data))

        with open(self.ymldir,"w+") as yml:
            data[0]['Options']['errorChoice'] = not data[0]['Options']['errorChoice']
            write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
            self.enablePrompts = data[0]['Options']['errorChoice']
            print(self.enablePrompts)
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

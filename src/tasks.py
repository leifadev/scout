import getpass
import os, logging
import wget, distro, platform
import shutil
import webbrowser
from datetime import datetime
from zipfile import ZipFile
import urllib.error
import ssl
import ruamel.yaml as yaml


class generalTasks:

    def __init__(self):
        self.changedDefaultDir = False
        self.thumbBool = False
        self.dirDefaultSetting = ""
        self.enablePrompts = True
        self.hasFilePrefix = False
        self.filePrefix = ""
        self.path = ""
        self.darkMode = False
        self.maxModeUse = 0
        self.logFont = "No value!"
        self.getUser = getpass.getuser()
        self.OS = distro.name(pretty=False)

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

        if "Windows" in platform.platform():
            self.OS = "Windows"
        else:
            pass

        """
        Auto-runs at start...

        Sets various variables for each OS being used.
        Fonts, directories, special boolean values, etc.
        """
        if self.OS not in "Windows Darwin":
            self.fileLoc = os.path.expanduser("~/.config/Scout/")
            self.dirDefaultSetting = "/home/" + self.getUser + "/Desktop"
            self.ymldir = os.path.expanduser("~/.config/Scout/settings.yml")
            self.cachedir = os.path.expanduser("~/.config/Scout/cache.yml")
            if self.path == "":
                self.path = "/home/" + self.getUser + "/Desktop"
            else:
                logging.warning(
                    "You don't have a selected path! Defaulting your desktop.\nFor more help use the help button to our github.")
            self.restartMsgY = None
            self.path_slash = "/"
            self.ffmpegDir = "ffmpeg"  # change this if you are downloading a seperate ffmpeg binary to config like macOS
            self.UIAttributes = {  # dictionarys for each OS to match aesthics
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
            if self.path == "":
                self.path = "/Users/" + self.getUser + "/Desktop"
            else:
                logging.warning(
                    "You don't have a selected path! Defaulting your desktop.\nFor more help use the help button to our github.")
            self.restartMsgY = None
            self.path_slash = "/"
            self.ffmpegDir = "/Users/" + self.getUser + "/Library/Application\ Support/Scout/ffmpeg"
            self.UIAttributes = {  # dictionarys for each OS to match aesthics
                "Font": "Source Code Pro",
                "charSize": 12,
                "restartTextPos": 302,
                "logFont": "Source Code Pro",
                "logSize": 10,
                "verSize": 12
            }

        elif self.OS in "Windows":  # change value for new platform object
            self.fileLoc = "C:\\Users\\" + self.getUser + "\\Appdata\\Roaming\\Scout\\"
            self.dirDefaultSetting = "C:\\Users\\" + self.getUser + "\Desktop"
            self.ymldir = "C:\\Users\\" + self.getUser + "\\AppData\\Roaming\\Scout\\settings.yml"
            self.cachedir = "C:\\Users\\" + self.getUser + "\\AppData\\Roaming\\Scout\\cache.yml"
            if self.path == "":
                self.path = "C:\\Users\\" + self.getUser + "\Desktop"
            else:
                logging.warning(
                    "You don't have a selected path! Defaulting your desktop.\nFor more help use the help button to our github.")
            self.restartMsgY = None
            self.path_slash = "\\"
            self.ffmpegDir = self.fileLoc + "ffmpeg"  # change this if you are downloading a seperate ffmpeg binary to config like macOS
            self.UIAttributes = {  # pre-made attributes to be place holders for multiple tkinter parames later on
                "Font": "Courier",
                "charSize": 8,
                "restartTextPos": 302,
                "logFont": "Courier",
                "logSize": 8,
                "verSize": 8
            }

        self.ffmpegDir = self.fileLoc + "ffmpeg"



    def genConfig(self):
        """
        Auto-runs at start...

        This generates the YML from scratch if its outdated or doesnt exist, and ignores otherwise.
        Uses sample yml "cache.yml" to compare it being the newest yml to a potentially old one.
        (Not enough or different settings).
        """

        # Generates initial yml file and folder, detects missing files as well
        if not os.path.isfile(self.fileLoc):
            path = os.path.join(self.fileLoc)
            logging.debug(os.getcwd())
            os.makedirs(path, exist_ok=True)
            logging.info("Folder generated...")
        if not os.path.isfile(self.ymldir) or os.path.getsize(self.ymldir) == 0:
            logging.info("Creating the settings.yml,\nThis is NOT a restored version of a previously deleted one!")
            os.chdir(self.fileLoc)
            logging.debug(os.getcwd())
            l = open("settings.yml", "w+")
            yaml.dump(self.payload, l, Dumper=yaml.RoundTripDumper)
            # yaml.dump(self.payload, f, Dumper=yaml.RoundTripDumper)
            l.close()
            print('\n\nDONEEE\n\n')

        # makes a copy of the newest yml/settings structure
        os.chdir(self.fileLoc)
        cache = open(self.cachedir, "w+")
        yaml.dump(self.payload, cache, Dumper=yaml.RoundTripDumper)
        logging.info("Cache updated!")


    def updateYML(self):
        """
        Auto-runs at start...

        Updating yml if is outdated with options (based on amount of keys)
        It basically fetches all current yml values and compares them to a clean new copy for the supposed newest installed version,
        If it find differences it will reset the settings to apply a new config.
        """

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
                # logging.info(f'\nCurrent Detect YML Options:\nSettings: {settingsList}\nCache: {cacheList}\n')
                # Checking if the newest YML is compatible, seeing a possibly older config, then updating it completely
                if settingsList == cacheList:
                    logging.info("Your settings.yml is up to date!\n")
                else:
                    with open(self.ymldir, "w+") as yml:
                        data = yaml.load(yml, Loader=yaml.Loader)
                        os.chdir(self.fileLoc)
                        cache = open("cache.yml", "w+")
                        cache.close()
                        yaml.dump(self.payload, yml, Dumper=yaml.RoundTripDumper)
                        logging.info("Cache updated!")

    def genLogo(self):
        logging.info("Attemping logo downloading...")
        url = "https://raw.githubusercontent.com/leifadev/scout/main/images/scout_logo.png"

        # Download icon for use if not present
        if not os.path.isfile(self.fileLoc + "scout_logo.png"):
            wget.download(url, self.fileLoc + "scout_logo.png")
        from tkinter import PhotoImage
        self.icon = PhotoImage(file=self.fileLoc + "scout_logo.png")

    # Dump function to write new values made by toggle buttons, etc.

    def dump(self, setting, var):
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)

            self.enablePrompts = data[0]['Options']['errorChoice']
            self.darkMode = data[0]['Options']['darkMode']
            self.filePrefix = data[0]['Options']['hasFilePrefix']
            self.thumbBool = data[0]['Options']['thumbnail']
            self.changedDefaultDir = False

            with open(self.ymldir, "w+") as yml:
                data[0]['Options'][setting] = not data[0]['Options'][setting]
                write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
                var = data[0]['Options'][setting]
                logging.debug(var, setting)

        logging.info("\nCurrently updating settings.yml...")


from tkinter.filedialog import *
from tkinter import messagebox

class guiTasks:

    def __init__(self):
        self.audioBool = False
        self.videoBool = False
        self.thumbBool = False
        self.filePrefix = False
        self.maxWarn = ""
        self.darkMode = False
        self.changedDefaultDir = False
        self.path = ""
        self.enablePrompts = False

    def switchMode(self):  # launches and toggles light and dark mode value
        logging.info("Click event successful!")

        if not self.darkMode:
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

            if not self.darkMode:
                self.maxWarn["fg"] = "#464646"  # light theme gray
                self.maxWarn["bg"] = "#ececec"
            else:
                self.maxWarn["fg"] = "#ececec"  # If statement checking if darkMode is on and to switch bg accordingly
                self.maxWarn["bg"] = "#464646"
            self.maxWarn.place(x=280, y=302, width=140)
            self.maxWarn["text"] = "Restart to apply!"
            self.menubar.entryconfig("About", state="disabled")
            self.maxWarn["font"] = tkFont.Font(family=self.UIAttributes.get("Font"),
                                               size=self.UIAttributes.get("charSize"))

    # This is function for the "File Destination" button in the main menu
    # Uses tkinter and fetches yml values to work

    def browseButton_command(self):
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.path = data[0]['Options'][
                'defaultDir']  # Fetch any set default directories specificed in settings pane
            self.changedDefaultDir = data[0]['Options']['changedDefaultDir']

        # First we load the data of the defaultDir value, regardless if we need it for the a selected default directory in settings by the user
        if self.changedDefaultDir:
            askdirectory(
                initialdir=self.path)  # If the default directory feature was used with a custom path, we will use it from the YML settings file
        else:
            logging.info("* Not using a default custom directory!")
            self.path = askdirectory(
                initialdir=self.path)  # Else if the boolean was false, we simply override the fetched self.path with the default desktop directory!
            self.path = self.dirDefaultSetting
        logging.info(self.path)

    # This includes changes boolean status for video/audio inclusion as well as handling the UI elements for them

    def videoButton_command(self):
        if not self.videoBool:
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
        logging.info("Video status: " + str(self.videoBool))

    # This includes changes boolean status for video/audio inclusion as well as handling the UI elements for them

    def audioButton_command(self):
        if not self.audioBool:
            self.audioBool = True
            if not self.videoBool:
                self.audioformat.place(x=650, y=220, width=75, height=30)
                self.audioquality.place(x=638, y=190, width=87, height=30)
        else:
            self.audioBool = False
            self.audioformat.place_forget()
            self.audioquality.place_forget()

        logging.info("Audio status: " + str(self.audioBool))

    # Help button takes user the github page, has wiki, code,issues, readme.md file and more

    def helpButton_command(self):
        webbrowser.open("https://github.com/leifadev/scout/wiki#help")
        self.logfield["state"] = "normal"
        self.logfield.insert(END, "\n\nINFO: Launched help page! Documentation, Code, Wiki, and more :)\n")
        self.logfield["state"] = "disabled"
        logging.info(
            "This is opening the github page to for Scout. All versions of scout, a public wiki, and an issues page\nare there to help!")

    # Clear the whole test entry, deleting line until the end, still restarting the welcome message!
    def clearConsole_command(self):
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.enablePrompts = data[0]['Options'][
                'errorChoice']  # Fetch any set default directories specificed in settings pane
        self.logfield["state"] = "normal"
        if self.enablePrompts:
            messagebox.showwarning("Warning", "Are you sure you want to clear the console?")
            self.logfield.delete("1.0", "end")
            self.logfield.insert(END,
                                 "Scout launched successfully!\nVersion: " + self.version + "\n" + f'OS: {self.OS}\n')
        else:
            self.logfield.delete("1.0", "end")
            self.logfield.insert(END,
                                 "Scout launched successfully!\nVersion: " + self.version + "\n" + f'OS: {self.OS}\n')
        self.logfield["state"] = "disabled"  # quickly disbaled user ability to edit log


    """
    Settings methods
    """

    def getTheme(self, name):
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.darkMode = data[0]['Options']['darkMode']
            if self.darkMode:
                name.set_theme("equilux")
            else:
                logging.info("No theme! Light mode then...")
                name["bg"] = "#ececec"


    def defaultDir_command(self):
        self.path = askdirectory()
        logging.info(f'\nSelected path: {self.path}')
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            with open(self.ymldir, "w+") as yml:
                self.changedDefaultDir = True
                data[0]['Options']['changedDefaultDir'] = self.changedDefaultDir
                data[0]['Options']['defaultDir'] = self.path
                write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)

    def resetDefaultDir_command(self):
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            with open(self.ymldir, "w+") as yml:
                self.changedDefaultDir = False
                data[0]['Options']['changedDefaultDir'] = self.changedDefaultDir
                data[0]['Options']['defaultDir'] = self.dirDefaultSetting  # done once reset
                write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)
                self.resetDefaultDir["state"] = "disabled"
                self.resetDirTip["text"] = "Setting reset!"
        logging.info("Reset the default directory in settings.")

    def togglePrefix(
            self):  # Coudln't use the function for this, sticking with the value being a string for the sake of it
        if self.prefixMenu['text'] == "Toggle On":
            self.filePrefix = ""
            self.prefixMenu["text"] = "Toggle Off"
            logging.info("Prefix off!")
        else:
            self.filePrefix = "Scout_"
            self.prefixMenu["text"] = "Toggle On"
            logging.info("Prefix on!")
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
        with open(self.ymldir, "r") as yml:
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

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

f = generalTasks()
f.genConfig()
f.updateYML()
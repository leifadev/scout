import tkinter as tk
from tkinter import ttk
from tkinter import (
    Label,
    Menu, Entry,
    Button, Checkbutton,
    OptionMenu, Text,
    PhotoImage, StringVar,
    CENTER, END
)

from tkinter.filedialog import *
from tkinter import messagebox
from ttkthemes import ThemedTk
import tkinter.font as tkFont
import webbrowser
import getpass, distro
import os, wget
import ruamel.yaml as yaml

from tasks import generalTasks, guiTasks


class App(generalTasks, guiTasks):

    def __init__(self, parent):

        super().__init__()
        self.fileLoc = ""
        self.videoBool = False
        self.audioBool = False
        self.videoRes = False
        self.hasFilePrefix = True
        self.path = ""
        self.darkMode = False
        self.maxModeUse = 0
        self.version = "v1.5"
        self.logFont = "No value!"
        self.getUser = getpass.getuser()
        self.OS = distro.name(pretty=False)
        self.videoq = ""  # vid quality example: 720p
        self.audioq = ""  # audio quality example: 128kbs
        self.videof = ""  # vid format example: mp4
        self.audiof = ""  # audio format example: wav

        ## Attributes ##

        parent.title("Scout")

        self.genLogo()
        parent.tk.call('wm', 'iconphoto', parent._w, self.icon)

        width = 845
        height = 350
        screenwidth = parent.winfo_screenwidth()
        screenheight = parent.winfo_screenheight()

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

        ## Menu items ##

        self.menubar = Menu(parent)
        self.filemenu = Menu(self.menubar, tearoff=0)

        try:
            self.filemenu.add_command(label="Cut", accelerator="Command+X",
                                      command=lambda: parent.focus_get().event_generate('<<Cut>>'))

            self.filemenu.add_command(label="Copy", accelerator="Command+C",
                                      command=lambda: parent.focus_get().event_generate('<<Copy>>'))

            self.filemenu.add_command(label="Paste", accelerator="Command+V",
                                      command=lambda: parent.focus_get().event_generate('<<Paste>>'))
            self.filemenu.add_command(label="Select All", accelerator="Command+A",
                                      command=lambda: parent.focus_get().select_range(0,
                                                                                      'END'))  # Does not work as of now v1.5
        except KeyError as e:
            self.logfield.insert(END, f"ERROR: Paste and copying functions failed! Try again?")
            print(f"Paste and copying functions failed!\n{e}")

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", accelerator="Command+Q", command=lambda: parent.quit())
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)

        self.helpmenu.add_command(label="About", command=self.aboutWindow())
        self.helpmenu.add_command(label="Help", command=self.helpButton_command)

        self.helpmenu.add_separator()

        self.helpmenu.add_command(label="Settings", command=self.settingsWindow)

        self.menubar.add_cascade(label="About", menu=self.helpmenu)

        self.menubar.entryconfig("About", state="normal")
        parent.config(menu=self.menubar)
        parent.update()  # Updates window at startup to be interactive and lifted, DO NOT TOUCH

        # self.menubar.entryconfig("Settings", state="disabled")

        ## Elements ##
        parent.lift()  # lift window to the top

        self.urlfield = ttk.Entry(parent)
        self.urlfield["justify"] = "left"
        self.urlfield["text"] = ""
        self.urlfield.insert(0, '')  # add pre made message
        self.urlfield.place(x=20, y=60, width=540)

        self.downloadButton = ttk.Button(parent)
        # self.downloadButton["justify"] = "center"
        self.downloadButton["text"] = "Download"
        self.downloadButton.place(x=570, y=59, width=120)
        self.downloadButton["command"] = self.downloadButton

        self.browseButton = ttk.Button(parent)
        self.browseButton["text"] = "File Destination"
        self.browseButton["command"] = self.browseButton_command
        self.browseButton.place(x=690, y=59, width=140)

        self.videoButton = tk.Checkbutton(parent)
        self.videoButton["text"] = "Video"
        self.videoButton.place(x=730, y=130, width=70, height=30)
        self.videoButton["offvalue"] = False
        self.videoButton["onvalue"] = True
        self.videoButton["command"] = self.videoButton_command

        self.audioButton = tk.Checkbutton(parent)
        self.audioButton["text"] = "Audio"
        self.audioButton.place(x=730, y=190, width=70, height=30)
        self.audioButton["offvalue"] = False
        self.audioButton["onvalue"] = True
        self.audioButton["command"] = self.audioButton_command

        helpButton = ttk.Button(parent)
        helpButton["text"] = "Help"
        helpButton.place(x=20, y=300, width=70)
        helpButton["command"] = self.helpButton_command

        clearButton = ttk.Button(parent)
        clearButton["text"] = "Clear"
        clearButton.place(x=95, y=300, width=70)
        clearButton["command"] = self.clearConsole_command

        self.modeButton = ttk.Button(parent)
        self.modeButton.place(x=170, y=300, width=100)
        self.modeButton["command"] = self.switchMode

        self.versionText = tk.Label(parent)
        self.versionText = Label(parent, text=self.version)
        self.versionText.place(x=740, y=300, width=125, height=30)
        self.versionText["font"] = tkFont.Font(family=self.UIAttributes.get("Font"),
                                               size=self.UIAttributes.get("verSize"))

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
        self.videoquality = ttk.OptionMenu(parent, self.clickedvq, "Quality", "1080p", "720p", "480p", "360p", "240p",
                                           "144p")
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
            self.versionText["bg"] = "#464646"  # dark theme gray
            self.versionText["fg"] = "#ececec"  # light theme gray

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
        with open(self.ymldir, "r") as yml:
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
        self.logfield.place(x=20, y=100, width=540, height=180)
        ft = tkFont.Font(family=self.UIAttributes.get("logFont"), size=self.UIAttributes.get("logSize"))
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(END, "Scout launched successfully!\nVersion: " + self.version + "\n" + f'OS: {self.OS}\n')
        self.logfield["state"] = "disabled"
        if self.darkMode:
            self.logfield["bg"] = "#e5e5e5"
        else:
            self.logfield[
                "bg"] = "#f6f6f6"  # if you want change this into 1 line for a bg dont keep it there for future adjustments

    # Settings pane UI and scripting
    def settingsWindow(self):  # Settings pane, offers customizable features!
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
        width = 550
        height = 400
        screenwidth = sWin.winfo_screenwidth()
        screenheight = sWin.winfo_screenheight()
        sWin_alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        sWin.geometry(sWin_alignstr)
        sWin.resizable(width=False, height=False)

        self.settingsTitle = ttk.Label(sWin)
        self.settingsTitle = Label(sWin, text="Settings")
        self.settingsTitle.place(x=207, y=10, width=140)
        if self.darkMode:
            self.settingsTitle["bg"] = "#464646"  # dark theme gray
            self.settingsTitle["fg"] = "#999999"  # light theme gray
        else:
            self.settingsTitle['bg'] = "#ececec"  # If statement checking if darkMode is on and to switch bg accordingly
            self.settingsTitle["fg"] = "black"

        self.defaultDirButton = ttk.Button(sWin, text="Choose")  # Disabled default dir until further notice
        self.defaultDirButton.place(x=287, y=50, width=120)
        self.defaultDirButton["command"] = self.defaultDir_command

        self.defaultDirTip = ttk.Label(sWin)
        self.defaultDirTip = Label(sWin, text="Set Default Directory")
        self.defaultDirTip.place(x=147, y=52, width=140)
        if self.darkMode:
            self.defaultDirTip["bg"] = "#464646"  # dark theme gray
            self.defaultDirTip["fg"] = "#999999"  # light theme gray
        else:
            self.defaultDirTip['bg'] = "#ececec"
            self.defaultDirTip["fg"] = "black"

        self.warnMenu = ttk.Button(sWin)
        self.warnMenu["text"] = "Toggle Off"
        self.warnMenu.place(x=292, y=92, width=110)
        self.warnMenu["command"] = self.errorToggle  # toggle button for prompts lolz

        self.warnTip = ttk.Label(sWin)
        self.warnTip = Label(sWin, text="Recieve Prompts")
        self.warnTip.place(x=165, y=92, width=110)
        if self.darkMode:
            self.warnTip["bg"] = "#464646"  # dark theme gray
            self.warnTip["fg"] = "#999999"  # light theme gray
        else:
            self.warnTip['bg'] = "#ececec"
            self.warnTip["fg"] = "black"

        self.prefixMenu = ttk.Button(sWin)
        self.prefixMenu["text"] = "Toggle Off"
        self.prefixMenu.place(x=292, y=137, width=110)
        self.prefixMenu["command"] = self.togglePrefix  # SECOND

        self.prefixTip = ttk.Label(sWin)
        self.prefixTip = Label(sWin, text="File Prefix")
        self.prefixTip.place(x=165, y=137, width=110)
        if self.darkMode:
            self.prefixTip["bg"] = "#464646"  # dark theme gray
            self.prefixTip["fg"] = "#999999"  # light theme gray
        else:
            self.prefixTip['bg'] = "#ececec"
            self.prefixTip["fg"] = "black"

        self.thumbMenu = ttk.Button(sWin)
        self.thumbMenu["text"] = "Toggle Off"
        self.thumbMenu.place(x=292, y=181, width=110)
        self.thumbMenu["command"] = self.toggleThumb

        self.thumbTip = ttk.Label(sWin)
        self.thumbTip = Label(sWin, text="Get Thumbnail")
        self.thumbTip.place(x=165, y=181, width=120)
        if self.darkMode:
            self.thumbTip["bg"] = "#464646"  # dark theme gray
            self.thumbTip["fg"] = "#999999"  # light theme gray
        else:
            self.thumbTip['bg'] = "#ececec"
            self.thumbTip["fg"] = "black"

        self.resetDefaultDir = ttk.Button(sWin)
        self.resetDefaultDir["text"] = "Reset Default Directory"
        self.resetDefaultDir.place(x=200, y=225, width=180)
        self.resetDefaultDir["command"] = self.resetDefaultDir_command
        self.resetDefaultDir["state"] = "normal"

        self.resetDirTip = ttk.Label(sWin)
        self.resetDirTip = Label(sWin, text="")
        self.resetDirTip.place(x=210, y=259, width=160)
        if self.darkMode:
            self.resetDirTip["bg"] = "#464646"  # dark theme gray
            self.resetDirTip["fg"] = "#999999"  # light theme gray
        else:
            self.resetDirTip['bg'] = "#ececec"
            self.resetDirTip["fg"] = "black"

        self.aprilFools = ttk.Label(sWin)
        self.aprilFools = Label(sWin, text="( ͡° ͜ʖ ͡°)", anchor=CENTER, wraplength=169, justify=CENTER)
        self.aprilFools["font"] = tkFont.Font(sWin, size=40)
        if self.darkMode:
            self.aprilFools["bg"] = "#464646"  # dark theme gray
            self.aprilFools["fg"] = "#999999"  # light theme gray
        else:
            self.aprilFools['bg'] = "#ececec"
            self.aprilFools["fg"] = "black"

        if "-04-01" in str(datetime.now()):
            self.aprilFools.place(x=190, y=290, width=200)
        else:
            pass

        # Updates buttons when they are loaded initially. Scroll down to enbd of button script section to see
        self.updateButtons()

    # About button UI and scripting
    def aboutWindow(self):
        abt = ThemedTk(themebg=True)
        abt.iconbitmap = PhotoImage(file=self.fileLoc + "scout_logo.png")
        self.getTheme(abt)
        abt.title("About")
        width = 300
        height = 300
        screenwidth = abt.winfo_screenwidth()
        screenheight = abt.winfo_screenheight()
        abt_alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        abt.geometry(abt_alignstr)
        abt.resizable(width=False, height=False)

        # Top 'Settings' title text
        self.abtTitle = ttk.Label(abt)
        self.abtTitle = Label(abt, text="About")
        self.abtTitle.place(x=45, y=10, width=210)
        if self.darkMode:
            self.abtTitle["bg"] = "#464646"  # dark theme gray
            self.abtTitle["fg"] = "#999999"  # light theme gray
        else:
            self.abtTitle['bg'] = "#ececec"
            self.abtTitle["fg"] = "black"

        ## All below are just the elements to the about pane, you can figure these out I'm sure :)
        abtMsg = "Author: leifadev\nLicense: GPL/GNU v3\nVersion: " + self.version + "\n\nLanguage: Python 3.6+\nCompilier: Pyinstaller\nFramework: Tkinter"
        self.msg = ttk.Label(abt)
        self.msg = Label(abt, text=abtMsg, anchor=CENTER, wraplength=160, justify=CENTER)
        self.msg.place(x=50, y=40, width=200)
        if self.darkMode:
            self.msg["bg"] = "#464646"  # dark theme gray
            self.msg["fg"] = "#999999"  # light theme gray
        else:
            self.msg['bg'] = "#ececec"
            self.msg["fg"] = "black"  # If statement checking if darkMode is on and to switch bg accordingly

        self.abtLink = "Contribute to the wiki!"
        self.abtLink = ttk.Label(abt)
        self.abtLink = Label(abt, font=(self.UIAttributes.get("Font"), self.UIAttributes.get("charSize"), "underline"),
                             text="Read the wiki for more info!", anchor=CENTER, wraplength=160, justify=CENTER)
        self.abtLink.place(x=50, y=170, width=200)
        self.abtLink["fg"] = "#2f81ed"
        self.abtLink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/leifadev/scout/wiki"))
        if self.darkMode:  # If statement checking if darkMode is on and to switch bg accordingly
            self.abtLink["bg"] = "#464646"  # dark theme gray
        else:
            self.abtLink['bg'] = "#ececec"


if __name__ == "__main__":
    parent = ThemedTk(themebg=True)
    app = App(parent)
    parent.mainloop()

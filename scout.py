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
import wget
import ssl
from sys import platform as _platform



class App:
    def __init__(self, root):
        self.audioBool = False
        self.videoBool = False
        self.changedDefaultDir = bool
        self.videoRes = False
        ssl._create_default_https_context = ssl._create_unverified_context

        self.version = "v1.3"

        # check OS
        if _platform == "linux" or _platform == "linux2":
            self.fileLoc = "/home/" + getpass.getuser() + "/Documents/"
            dirDefaultSetting = "~/Desktop"
            self.ymldir = "/home/" + getpass.getuser() + "/Documents/Scout/settings.yml"


        elif _platform == "darwin":
            self.fileLoc = "/Users/" + getpass.getuser() + "/Library/Application Support/"
            dirDefaultSetting = "~/Desktop"
            self.ymldir = "/Users/" + getpass.getuser() + "/Library/Application Support/Scout/settings.yml"


        elif _platform == "win64" or "win32":
            self.fileLoc = "C:\\Users\\" + getpass.getuser() + "\\Appdata\\Roaming\\"
            dirDefaultSetting = "C:\\Users\\" + getpass.getuser() + "\Desktop"
            self.ymldir = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\Scout\\settings.yml"



        # Database (pre-made yml structure for intial generation)
        self.payload = [
            {
                'Options': {
                    'defaultDir': dirDefaultSetting,
                    'errorChoice': True,
                    'changedDefaultDir': False
                }
            }
        ]



        # Generates initial yml file and folder, detects missing files as well
        if not os.path.isfile(self.fileLoc + "Scout"):
            path = os.path.join(self.fileLoc, "Scout")
            os.makedirs(path, exist_ok=True)
            print("Folder generated...")
        if not os.path.isfile(self.ymldir):
            print("Creating settings.yml,\nThis is not a restored version of a previously deleted one!")
            os.chdir(self.fileLoc + "scout")
            print(os.getcwd())
            f = open("settings.yml","w+")
            f.close
            yaml.dump(self.payload, f, Dumper=yaml.RoundTripDumper)


        # Organizing and downloading app icon #

        print("Attemping logo downloading...")
        url = "https://raw.githubusercontent.com/leifadev/scout/main/scout_logo.png"

        if _platform == "linux" or _platform == "linux2":
            print("unix gen")
            if not os.path.isfile(self.fileLoc + "Scout/scout_logo.png"):
                wget.download(url, self.fileLoc + "Scout/scout_logo.png")
            icon = PhotoImage(file=self.fileLoc + "Scout/scout_logo.png")



        elif _platform == "darwin":
            if not os.path.isfile(self.fileLoc + "Scout/scout_logo.png"):
                wget.download(url, self.fileLoc + "Scout/scout_logo.png")
            icon = PhotoImage(file=self.fileLoc + "Scout/scout_logo.png")



        elif _platform == "win64" or "win32":
            print("win gen")
            if not os.path.isfile(self.fileLoc + "Scout\\scout_logo.png"):
                wget.download(url, self.fileLoc + "Scout\\scout_logo.png")
            icon = PhotoImage(file="C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\Scout\\scout_logo.png")



        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.enablePrompts = data[0]['Options']['errorChoice']
    



        ## UI elements ##

        # Attributes #

        root.title("Scout")
        root.tk.call('wm', 'iconphoto', root._w, icon)
        width=845
        height=350
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)


        # Menu items

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
        helpmenu.add_command(label="About")
        helpmenu.add_command(label="Help", command=self.helpButton_command)

        helpmenu.add_separator()

        helpmenu.add_command(label="Settings", command=self.settings_button)
        menubar.add_cascade(label="About", menu=helpmenu)

        root.config(menu=menubar)
        root.update()   # Updates window at startup to be interactive and lifted, DO NOT TOUCH


        # Elements #

        root.lift()

        self.urlfield = tk.Entry(root)
        self.urlfield["justify"] = "left"
        self.urlfield["text"] = ""
        self.urlfield.insert(0, '')   # add pre made message
        self.urlfield.place(x=20,y=60,width=540)

        self.downloadButton=tk.Button(root)
        self.downloadButton["justify"] = "center"
        self.downloadButton["text"] = "Download"
        self.downloadButton.place(x=570,y=59,width=120)
        self.downloadButton["command"] = self.downloadButton_command


        self.browseButton=tk.Button(root)
        self.browseButton["text"] = "File Destination"
        self.browseButton["command"] = self.browseButton_command
        self.browseButton.place(x=690,y=59,width=140)


        self.videoButton=tk.Checkbutton(root)
        self.videoButton["justify"] = "center"
        self.videoButton["text"] = "Video"
        self.videoButton.place(x=720,y=120,width=70,height=25)
        self.videoButton["offvalue"] = False
        self.videoButton["onvalue"] = True
        self.videoButton["command"] = self.videoButton_command

        self.audioButton=tk.Checkbutton(root)
        self.audioButton["justify"] = "center"
        self.audioButton["text"] = "Audio"
        self.audioButton.place(x=720,y=160,width=70,height=25)
        self.audioButton["offvalue"] = False
        self.audioButton["onvalue"] = True
        self.audioButton["command"] = self.audioButton_command

        helpButton=tk.Button(root)
        helpButton["justify"] = "center"
        helpButton["text"] = "Help"
        helpButton.place(x=20,y=300,width=70)
        helpButton["command"] = self.helpButton_command

        clearButton=tk.Button(root)
        helpButton["justify"] = "center"
        clearButton["text"] = "Clear"
        clearButton.place(x=95,y=300,width=70)
        clearButton["command"] = self.clearConsole_command

        self.versionText = tk.Label(root)
        self.versionText = Label(root, text=self.version)
        self.versionText.place(x=780,y=300,width=70,height=25)
        self.versionText["font"] = tkFont.Font(family='Source Code Pro', size=9)


        ## LOG FEILD AND ERROR HANDLING ##

        self.logfield = tk.Text(root)
        self.logfield.place(x=20,y=100,width=540, height=180)
        ft = tkFont.Font(family='Source Code Pro', size=10)
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(INSERT, "Scout launched successfully!\nVersion: " + self.version + "\n")
        self.logfield["bg"] = "#F6F6F6"
        self.logfield["state"] = "disabled"


    ########################################################################################################

    ## Triggers and Scripts ##

    def videoFetch(self, yt, query): # Basic video basic report (used in all download types)
        yt = YouTube(query)
        query = self.urlfield.get()
        self.logfield.insert(INSERT, f'\n\nStarting download to path: {self.path}')
        self.logfield.insert(INSERT, f'\nVideo Author: {yt.author}')
        self.logfield.insert(INSERT, f'\nPublish Date: {yt.publish_date}')
        self.logfield.insert(INSERT, f'\nVideo Duration (sec): {yt.length}')
        self.logfield.insert(INSERT, f'\nViews: {yt.views}')
        self.logfield.insert(INSERT, f'\nRating ratio: {yt.rating}')
        self.logfield.insert(INSERT, f'\n\n---------------------------------------------------------------------\n\n')

        self.logfield["state"] = "disabled" # quickly disbaled user ability to edit log


    def downloadButton_command(self):
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
                videoDown = yt.streams.filter().get_highest_resolution()
                videoDown.download(self.path, filename_prefix="Scout_")
                comp = videoDown.on_complete(self.path)

                self.logfield.insert(INSERT, f'INFO: vcodec="avc1.64001e", res="highest", fps="best", format="video/mp4"\n')
                self.videoFetch(yt, query)

            except VideoPrivate:
                self.logfield.insert(INSERT, f'\nERROR: This video is privated, you can\'t download it\n')
            except RegexMatchError:
                self.logfield.insert(INSERT, f'\nERROR: Invalid link formatting\n')
            except VideoRegionBlocked:
                self.logfield.insert(INSERT, f'\nERROR: This video is block in your region\n')
            except RecordingUnavailable:
                self.logfield.insert(INSERT, f'\nERROR: This recording is unavalilable\n')
            except MembersOnly:
                self.logfield.insert(INSERT, f'\nERROR: This video is for channel members only.\nRefer here for more info: https://support.google.com/youtube/answer/7544492\n')
            except LiveStreamError:
                self.logfield.insert(INSERT, f'\nERROR: This is a livestream, and not a downloadable video\n')
            except HTMLParseError:
                self.logfield.insert(INSERT, f'\nERROR: HTML parsing or extraction has failed')
            except VideoUnavailable:
                self.logfield.insert(INSERT, f'\nERROR: This video is unavalilable, may possibly be payed material or region-locked\n')
            self.logfield["state"] = "disabled"



        elif self.audioBool:  # Audio only
            self.logfield["state"] = "normal"

            try:
                yt = YouTube(query)
                query = self.urlfield.get()
                audioDown = yt.streams.filter(only_audio=True).first()
                audioDown.download(self.path, filename_prefix="Scout_")

                self.logfield.insert(INSERT, f'\nINFO: vcodec="avc1.64001e", format="audio/mp4"\n')
                self.videoFetch(yt, query)

            except VideoPrivate:
                self.logfield.insert(INSERT, f'\nERROR: This video is privated, you can\'t download it\n')
            except VideoRegionBlocked:
                self.logfield.insert(INSERT, f'\nERROR: This video is block in your region\n')
            except RegexMatchError:
                self.logfield.insert(INSERT, f'\nERROR: Invalid link formatting\n')
            except RecordingUnavailable:
                self.logfield.insert(INSERT, f'\nERROR: This recording is unavalilable\n')
            except MembersOnly:
                self.logfield.insert(INSERT, f'\nERROR: This video is for channel members only.\nRefer here for more info: https://support.google.com/youtube/answer/7544492\n')
            except LiveStreamError:
                self.logfield.insert(INSERT, f'\nERROR: This is a livestream, and not a downloadable video\n')
            except HTMLParseError:
                self.logfield.insert(INSERT, f'\nERROR: HTML parsing or extraction has failed')
            except VideoUnavailable:
                self.logfield.insert(INSERT, f'\nERROR: This video is unavalilable, may possibly be payed material or region-locked\n')
            self.logfield["state"] = "disable"


            # high_audioDown = yt.streams.get_audio_only()


        elif self.audioBool == False and self.videoBool: # Video only
            self.logfield["state"] = "normal"
            if self.enablePrompts:
                messagebox.showwarning("Warning", "Video resolutions for this option are lower quailty.")
                self.logfield.insert(INSERT, f'\nINFO: As of now videos downloaded without audio are fixed to 360p\n')
            try:
                yt = YouTube(query)
                query = self.urlfield.get()
                silent_audioDown = yt.streams.filter(only_video=True).get_by_itag(itag=134)
                silent_audioDown.download(self.path, filename_prefix="Scout_")

                self.logfield.insert(INSERT, f'\nINFO: vcodec="avc1.4d401e", res_LOW="360p", fps="24fps", format="video/mp4"')
                self.videoFetch(yt, query)

            except VideoPrivate:
                self.logfield.insert(INSERT, f'\nERROR: This video is privated, you can\'t download it\n')
            except VideoRegionBlocked:
                self.logfield.insert(INSERT, f'\nERROR: This video is block in your region\n')
            except RegexMatchError:
                self.logfield.insert(INSERT, f'\nERROR: Invalid link formatting\n')
            except RecordingUnavailable:
                self.logfield.insert(INSERT, f'\nERROR: This recording is unavalilable\n')
            except MembersOnly:
                self.logfield.insert(INSERT, f'\nERROR: This video is for channel members only.\nRefer here for more info: https://support.google.com/youtube/answer/7544492\n')
            except LiveStreamError:
                self.logfield.insert(INSERT, f'\nERROR: This is a livestream, and not a downloadable video\n')
            except HTMLParseError:
                self.logfield.insert(INSERT, f'\nERROR: HTML parsing or extraction has failed')
            except VideoUnavailable:
                self.logfield.insert(INSERT, f'\nERROR: This video is unavalilable, may possibly be payed material or region-locked\n')
            self.logfield["state"] = "disabled"

        else:
            self.logfield["state"] = "normal"

            query = self.urlfield.get() # gets entry input

            if self.urlfield.get() == "":
                self.logfield.insert(INSERT, f'\nERROR: URL field is empty and cannot be parsed')

            elif self.enablePrompts: # hasnt selected video nor audio
                self.logfield.insert(INSERT, f'\nERROR: You can\'t download a video with video or audio\n')

            self.logfield["state"] = "disabled"



    ########################################################################################################


    def browseButton_command(self):
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.path = data[0]['Options']['defaultDir']

        if self.changedDefaultDir:
            askdirectory(initialdir=self.path)
        else:
            askdirectory(initialdir='/Users/' + getpass.getuser() + '/Desktop/')


    def videoButton_command(self):
        if self.videoBool == False:
            self.videoBool = True
        else:
            self.videoBool = False


    def audioButton_command(self):
        if self.audioBool == False:
            self.audioBool = True
        else:
            self.audioBool = False

    def helpButton_command(self):
        webbrowser.open("https://github.com/leifadev/scout")


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


    def settings_button(self): # Settings pane, offers custiomizable features!
        sWin = Tk()
        sWin.title("Settings")
        width=550
        height=400
        screenwidth = sWin.winfo_screenwidth()
        screenheight = sWin.winfo_screenheight()
        sWin_alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        sWin.geometry(sWin_alignstr)
        sWin.resizable(width=False, height=False)

        defaultDirTip = tk.Label(sWin)
        defaultDirTip = Label(sWin, text="Settings")
        defaultDirTip.place(x=207,y=10,width=140)

        self.defaultDirButton=tk.Button(sWin, text="Choose") # Disabled default dir until further notice
        self.defaultDirButton["justify"] = "center"
        #        self.defaultDirButton["text"] = "Choose"
        self.defaultDirButton.place(x=287,y=50,width=120)
        self.defaultDirButton["command"] = self.defaultDir_command

        self.defaultDirTip = tk.Label(sWin)
        self.defaultDirTip = Label(sWin, text="Set Default Directory")
        self.defaultDirTip.place(x=147,y=50,width=140)

        self.warnMenu = tk.Button(sWin)
        self.warnMenu["justify"] = "center"


        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader) # Changing button state depending on mode
            if data[0]['Options']['errorChoice']:
                self.warnMenu["text"] = "Toggle On"
            else:
                self.warnMenu["text"] = "Toggle Off"


        self.warnMenu["text"] = "Toggle Off"
        self.warnMenu.place(x=280,y=102,width=110)
        self.warnMenu["command"] = self.errorToggle


        self.defaultDirTip = tk.Label(sWin)
        self.defaultDirTip = Label(sWin, text="Recieve Prompts")
        self.defaultDirTip.place(x=165,y=103,width=110)



    def defaultDir_command(self):
        self.path = askdirectory()
        print(self.path)
        with open(self.ymldir,"r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)

        with open(self.ymldir,"w+") as yml:
            data[0]['Options']['changedDefaultDir'] = True
            data[0]['Options']['defaultDir'] = self.path
            write = yaml.dump(data, yml, Dumper=yaml.RoundTripDumper)


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

# https://python-pytube.readthedocs.io/en/latest/api.html


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

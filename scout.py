import tkinter as tk
from tkinter import *
import webbrowser
from tkinter.filedialog import askdirectory
from pytube import YouTube     # pip3 install pytube3
import pytube
import getpass
from tkinter import messagebox
import yaml
import os
import tkinter.font as tkFont
from pytube.exceptions import VideoUnavailable



# python3 setup.py py2app -A
# The whole app with its enity is in class App. Didn't deel the need to make more or something... lol


class App:
    def __init__(self, root):
        self.audioBool = False
        self.videoBool = False
        self.changedDefaultDir = bool
        self.path = '/Users/' + getpass.getuser() + '/Desktop/' #macos dir

        self.videoRes = False


        # Database
        self.fileLoc = "/Users/" + getpass.getuser() + "/Library/Application Support/Scout/settings.yml"
        self.payload = {
            'Options': {
                'defaultDir': self.fileLoc,
                'errorChoice': True,
                'changedDefaultDir': False
            }
        }

        self.enablePrompts = self.payload['Options']['errorChoice']


        if os.path.exists(self.fileLoc): # Check to dump on startup
            pass
        else:
            self.dump()



        #        print(tk.font.families())

        ## UI elements ##

        # Attributes #

        root.title("Scout")
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


        # Elements #

        #        label = tk.Label(root)
        #        label["justify"] = "left"
        #        label["text"] = "Scout"
        #        #        label.pack(padx=1,pady=2)
        #        label.place(x=390,y=5,width=70,height=25)

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


        logevents = []




        ## LOG FEILD AND ERROR HANDLING ##

        self.logfield = tk.Text(root)
        self.logfield.place(x=20,y=100,width=540, height=180)
        ft = tkFont.Font(family='Source Code Pro', size=10)
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(INSERT, "Scout launched successfully!")
#        self.logfield["state"] = "disabled" # Put this LAST to all logging statements!
        self.logfield["bg"] = "#F6F6F6"


    ########################################################################################################


    ## Triggers and Scripts ##
    try:
        def downloadButton_command(self):
            if self.urlfield.get() == "":
                messagebox.showerror("Error", "Please enter a URL!")
            query = self.urlfield.get() # gets entry input

            if self.videoBool and self.audioBool: # Video and Audio
                yt = YouTube(query)
                videoDown = yt.streams.filter().get_highest_resolution()
                videoDown.download(self.path, filename_prefix="Scout_")

            elif self.audioBool:  # Audio only
                query = self.urlfield.get()
                yt = YouTube(query)

                audioDown = yt.streams.filter(only_audio=True).first()
                audioDown.download(self.path, filename_prefix="Scout_")
                # high_audioDown = yt.streams.get_audio_only()

            elif self.audioBool == False and self.videoBool: # Video only
                if self.enablePrompts:
                    messagebox.showwarning("Warning", "Video resolutions for this option are lower quailty.")


                query = self.urlfield.get()
                yt = YouTube(query)

                silent_audioDown = yt.streams.filter(only_video=True).get_by_itag(itag=134)
                silent_audioDown.download(self.path, filename_prefix="Scout_")

            else:
                if self.enablePrompts:
                    messagebox.showerror("Error", "Invalid selection, you need download a form of media!")

    except VideoPrivate:
        print("COOL")


#                self.logfield.insert(INSERT, f'\nTitle: {yt.title}')
#                self.logfield.insert(INSERT, f'\nVideo Author: {yt.author}')
#                self.logfield.insert(INSERT, f'\nPublish Date: {yt.publish_date}')
#                self.logfield.insert(INSERT, f'\nVideo Duration: {yt.length}')
#                self.logfield.insert(INSERT, f'\nViews: {yt.views}')
#                self.logfield.insert(INSERT, f'\nRating: {yt.rating}')
#                self.logfield.insert(INSERT, f'\nThumbnail URL: {yt.thumbnail_url}')
#
#                self.logfield["state"] = "disabled" # Put this LAST to all logging statements!
        
        
        
    ########################################################################################################


    def browseButton_command(self):
        if self.changedDefaultDir != False:
            askdirectory(initialdir=self.path)
        else:
            print(self.changedDefaultDir)
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




    def settings_button(self):
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

        self.defaultDirButton=tk.Button(sWin, text="Choose", state=tk.DISABLED) # Disabled default dir until further notice
        self.defaultDirButton["justify"] = "center"
        #        self.defaultDirButton["text"] = "Choose"
        self.defaultDirButton.place(x=287,y=48,width=120)
        self.defaultDirButton["command"] = self.defaultDir_command

        self.defaultDirTip = tk.Label(sWin)
        self.defaultDirTip = Label(sWin, text="Set Default Directory")
        self.defaultDirTip.place(x=147,y=50,width=140)

        self.warnMenu = tk.Button(sWin)
        self.warnMenu["justify"] = "center"
        self.warnMenu["text"] = "Toggle Off"
        self.warnMenu.place(x=280,y=100,width=110)
        self.warnMenu["command"] = self.errorToggle

        self.defaultDirTip = tk.Label(sWin)
        self.defaultDirTip = Label(sWin, text="Recieve Prompts")
        self.defaultDirTip.place(x=165,y=103,width=110)



    def defaultDir_command(self):
        self.path = str(askdirectory())   # Uses tkinter filedialog for prompting a save dir
        if self.changedDefaultDir:
            self.changedDefaultDir = True


    def errorToggle(self):
        if self.enablePrompts == False:
            self.enablePrompts = True
        else:
            self.enablePrompts = False

        if self.enablePrompts:
            self.warnMenu["text"] = "Toggle Off"
        else:
            self.warnMenu["text"] = "Toggle On"

        self.payload['Options']['errorChoice'] = self.enablePrompts
        self.dump()


    def dump(self):
        with open(self.fileLoc, 'w') as settingsFile:
            dump = yaml.dump(self.payload, settingsFile)


# https://python-pytube.readthedocs.io/en/latest/api.html



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
